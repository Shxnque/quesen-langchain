"""
Fail-closed enforcement decorator for LangChain / LangGraph.

v0.4.0 tracks quesen-sdk 0.5.0. This closes the "advisory-only" gap: a tool the
agent is *told* to call before acting is only as good as the agent's compliance.
`quesen_guard` wraps ``quesen_sdk.QuesenFirewall.guard`` so ANY Python callable
(a LangChain tool's function, a LangGraph node, a plain helper) executes ONLY
when Quesen returns PASS for the described action. On BLOCK / REVIEW / SKIP
(or transport error) the body never runs and ``quesen_sdk.tsc.TscBlocked`` is
raised (fail-closed). The verdict is attached to the wrapped callable as
``.last_decision`` for auditing.

Example::

    from quesen_langchain import quesen_guard

    @quesen_guard(base_url="https://<engine>", sandbox=True,
                  action="payment", trust_tier="unverified")
    def send_funds(to: str, amount: float) -> str:
        ...  # only runs on PASS

    send_funds("0xabc", 5)          # raises TscBlocked unless PASS
    send_funds.last_decision        # the TscDecision (audit receipt)

Per-call overrides may be supplied via the ``_quesen`` kwarg::

    send_funds("0xabc", 5, _quesen={"target": "0xabc"})

Doctrine anchors: §2 Determinism preserved (no ML in the wrapper); fail-closed.
"""
from __future__ import annotations

from typing import Any, Optional

try:
    from quesen_sdk import QuesenClient, QuesenFirewall
except ImportError as exc:  # pragma: no cover
    raise ImportError(
        "quesen-langchain requires `quesen-sdk>=0.5.0`. Install with `pip install quesen-langchain`."
    ) from exc

__all__ = ["quesen_guard"]


def quesen_guard(
    *,
    base_url: Optional[str] = None,
    api_key: Optional[str] = None,
    sandbox: bool = False,
    client: Optional[QuesenClient] = None,
    firewall: Optional[QuesenFirewall] = None,
    timeout: float = 5.0,
    retries: int = 2,
    **action: Any,
):
    """Return a fail-closed enforcement decorator bound to a Quesen firewall.

    The ``**action`` kwargs describe the high-risk action to evaluate and are
    forwarded verbatim to :meth:`quesen_sdk.QuesenFirewall.check` (e.g.
    ``action='send_data'``, ``target=...``, ``data_class='secret'``,
    ``capability_class=...``, ``granted_scopes=...``, ``trust_tier=...``).
    """
    fw = firewall
    if fw is None:
        if client is not None:
            fw = QuesenFirewall(client=client)
        elif sandbox and not api_key:
            fw = QuesenFirewall.sandbox(base_url, timeout=timeout, retries=retries)
        else:
            fw = QuesenFirewall(
                base_url=base_url, api_key=api_key, timeout=timeout, retries=retries
            )
    return fw.guard(**action)
