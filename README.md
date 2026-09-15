# Quesen — LangChain / LangGraph Tool

> Deterministic **Agent Firewall** + A2A risk validation as LangChain `BaseTool`s. **Integrate in under 5 minutes.**

**Status:** v0.3.0 · tracks Quesen engine v1.10.0 (TSC v2 firewall) · requires `quesen-sdk>=0.4.1`.
**Developer portal:** https://senueren.co.za/quesen · **Source:** https://github.com/Shxnque/quesen

---

## Agent Firewall (30-second, no signup)

```python
from quesen_langchain import QuesenFirewallTool

# sandbox=True self-serves a free key against the hosted engine.
firewall = QuesenFirewallTool(
    base_url="https://web-production-3df26.up.railway.app",
    sandbox=True,
)

# Give it to any LangChain/LangGraph agent, or call directly:
verdict = firewall._run(
    agent="my-agent", action="send_data",
    target="https://paste.evil.example", data_class="secret",
)
print(verdict["decision"])                       # 'BLOCK'
print([r["code"] for r in verdict["reasons"]])   # ['EGRESS_SECRET_UNTRUSTED']
```

`action` accepts `send_data` / `tool_call` / `payment` (+ aliases). For production
pass `api_key="sk_live_..."` instead of `sandbox=True`.


---

## Install

```bash
pip install quesen-langchain
# or from source while we publish:
pip install git+https://github.com/Shxnque/quesen-langchain.git
```

Brings `quesen-sdk>=0.2.0` and `langchain-core` with it. No LLM lock-in.

---

## 30-second usage

```python
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from quesen_langchain import QuesenValidateTool, QuesenReportTool

validate_tool = QuesenValidateTool(base_url="https://<your-quesen>", api_key="sk_live_abc")
report_tool   = QuesenReportTool(base_url="https://<your-quesen>", api_key="sk_live_abc")

agent = ChatOpenAI(model="gpt-4o-mini").bind_tools([validate_tool, report_tool])
print(agent.invoke([HumanMessage("Should I ape into a 1-day-old token with 4 scam keywords and 95% engagement?")]))
```

---

## Receipt provenance (v1.10, tracked in v0.2.0)

`QuesenValidateTool._run(...)` returns the raw response dict verbatim from the
underlying `quesen-sdk` client. When talking to a v1.10.0+ engine that dict
includes two additional fields:

- `input_snapshot_hash` — 64-char SHA-256 hex over the canonical request payload.
- `commit_sha` — 40-char git SHA of the engine ruleset live at decision time (or `"unknown"`).

Both flow through unchanged for downstream LangGraph nodes to consume, log, or
verify. See the [developer portal API reference](https://github.com/Shxnque/quesen/blob/main/docs/api-reference.md#receipt-provenance-v110)
for the field contract.

---

## What ships

| Tool | Wraps | Purpose |
|---|---|---|
| `QuesenValidateTool` | `POST /validate` | Deterministic PROCEED/REVIEW/SKIP verdict (carries v1.10 provenance) |
| `QuesenSimulateTool` | `POST /simulate` | Free counterfactual (test the model without spending a call) |
| `QuesenReportTool` | `POST /report` | Post-decision outcome feedback (v1.1 schema) |

All three are `langchain_core.tools.BaseTool` subclasses with structured Pydantic inputs. Compatible with LangGraph, `create_react_agent`, `bind_tools()`, and every LangChain callback pipeline.

---

## Environment

| Var | Meaning |
|---|---|
| `QUESEN_BASE_URL` | Optional default base URL (else pass to the tool constructor). |
| `QUESEN_API_KEY`  | Optional default API key. |

---

## Doctrine compliance (inherited from parent)

- **Determinism.** No prompt-tuning, no randomness in the wrapper.
- **Ecosystem neutrality.** Depends on `langchain-core` only, not on any specific LLM provider.
- **Fail-closed.** Timeouts surface as tool errors; recommended agent policy: treat as `SKIP`.
- **Provenance forwarded.** The raw dict returned to the LangChain runtime carries `input_snapshot_hash` and `commit_sha` unchanged, so downstream nodes can pin the ruleset.

MIT license. See [`senueren.co.za/quesen`](https://senueren.co.za/quesen) for canonical documentation.
