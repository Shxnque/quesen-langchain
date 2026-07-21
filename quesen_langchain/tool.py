"""
LangChain / LangGraph BaseTool wrappers around the Quesen Python SDK.

Every tool is a thin, deterministic wrapper: no prompt tuning, no state,
no LLM in the loop. Same input in → same input out (up to the request_id).

Doctrine anchors (see https://senueren.co.za/quesen for public design principles):
- §2 Determinism preserved.
- §11 Ecosystem neutrality: depends on langchain-core (not langchain-openai etc.).
- Fail-closed: SDK errors surface unchanged so the caller decides policy.
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Type

try:
    from langchain_core.tools import BaseTool
    from pydantic import BaseModel, Field
except ImportError as exc:  # pragma: no cover
    raise ImportError(
        "quesen-langchain requires `langchain-core` and `pydantic`. "
        "Install with `pip install quesen-langchain`."
    ) from exc

try:
    from quesen_sdk import QuesenClient
except ImportError as exc:  # pragma: no cover
    raise ImportError(
        "quesen-langchain requires `quesen-sdk`. Install with `pip install quesen-sdk`."
    ) from exc


# --------------------- Input schemas ---------------------

class _ValidateInput(BaseModel):
    domain_age_days: Optional[int] = Field(default=None, ge=0)
    engagement_ratio: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    scam_keyword_count: Optional[int] = Field(default=None, ge=0)
    client_request_id: Optional[str] = Field(default=None, max_length=128)


class _SimulateInput(BaseModel):
    domain_age_days: Optional[int] = Field(default=None, ge=0)
    engagement_ratio: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    scam_keyword_count: Optional[int] = Field(default=None, ge=0)
    weights_override: Optional[Dict[str, float]] = None
    thresholds_override: Optional[Dict[str, float]] = None


class _ReportInput(BaseModel):
    request_id: str = Field(min_length=1, max_length=128)
    outcome: str = Field(description="RUG | LOSS | OK | WIN | UNKNOWN")
    notes: Optional[str] = Field(default=None, max_length=1000)
    realized_pnl: Optional[float] = None
    elapsed_seconds: Optional[int] = Field(default=None, ge=0)
    venue: Optional[str] = Field(default=None, max_length=64)
    signal_hash: Optional[str] = Field(default=None, max_length=128)


# --------------------- Base ---------------------

class _BaseQuesenTool(BaseTool):
    """Shared client management for the three Quesen tools."""

    base_url: Optional[str] = None
    api_key: Optional[str] = None
    timeout: float = 5.0
    retries: int = 2

    _client: Optional[QuesenClient] = None  # populated lazily

    def _get_client(self) -> QuesenClient:
        if self._client is None:
            self._client = QuesenClient(
                base_url=self.base_url,
                api_key=self.api_key,
                timeout=self.timeout,
                retries=self.retries,
            )
        return self._client


# --------------------- Concrete tools ---------------------

class QuesenValidateTool(_BaseQuesenTool):
    """Deterministic PROCEED / REVIEW / SKIP verdict for an opportunity."""

    name: str = "quesen_validate"
    description: str = (
        "Deterministic A2A risk validation. Call BEFORE taking a financial or "
        "high-consequence action. Returns PROCEED / REVIEW / SKIP with a risk_score, "
        "confidence, and named conflict_triggers. Same input -> same output."
    )
    args_schema: Type[BaseModel] = _ValidateInput

    def _run(self, **kwargs: Any) -> Dict[str, Any]:
        c = self._get_client()
        r = c.validate(
            domain_age_days=kwargs.get("domain_age_days"),
            engagement_ratio=kwargs.get("engagement_ratio"),
            scam_keyword_count=kwargs.get("scam_keyword_count"),
            client_request_id=kwargs.get("client_request_id"),
        )
        return r.raw

    async def _arun(self, **kwargs: Any) -> Dict[str, Any]:  # pragma: no cover
        return self._run(**kwargs)


class QuesenSimulateTool(_BaseQuesenTool):
    """Counterfactual scoring — free, uses /simulate. Great for calibration."""

    name: str = "quesen_simulate"
    description: str = (
        "Free counterfactual scoring. Provide the signals and optional "
        "weights_override / thresholds_override; get baseline vs simulated "
        "decisions and the delta. Not charged against your API key."
    )
    args_schema: Type[BaseModel] = _SimulateInput

    def _run(self, **kwargs: Any) -> Dict[str, Any]:
        c = self._get_client()
        r = c.simulate(
            domain_age_days=kwargs.get("domain_age_days"),
            engagement_ratio=kwargs.get("engagement_ratio"),
            scam_keyword_count=kwargs.get("scam_keyword_count"),
            weights_override=kwargs.get("weights_override"),
            thresholds_override=kwargs.get("thresholds_override"),
        )
        return r.raw

    async def _arun(self, **kwargs: Any) -> Dict[str, Any]:  # pragma: no cover
        return self._run(**kwargs)


class QuesenReportTool(_BaseQuesenTool):
    """Post-decision outcome feedback (v1.1 schema)."""

    name: str = "quesen_report"
    description: str = (
        "Report the realized outcome of a decision back to Quesen. Pass the "
        "request_id from the /validate response + an outcome enum "
        "(RUG|LOSS|OK|WIN|UNKNOWN). Optional post-trade metadata improves the "
        "model over time."
    )
    args_schema: Type[BaseModel] = _ReportInput

    def _run(self, **kwargs: Any) -> Dict[str, Any]:
        c = self._get_client()
        r = c.report(
            request_id=kwargs["request_id"],
            outcome=kwargs["outcome"],
            notes=kwargs.get("notes"),
            realized_pnl=kwargs.get("realized_pnl"),
            elapsed_seconds=kwargs.get("elapsed_seconds"),
            venue=kwargs.get("venue"),
            signal_hash=kwargs.get("signal_hash"),
        )
        return r.raw

    async def _arun(self, **kwargs: Any) -> Dict[str, Any]:  # pragma: no cover
        return self._run(**kwargs)
