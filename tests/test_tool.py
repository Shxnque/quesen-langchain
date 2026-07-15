"""LangChain wrapper smoke tests (structure-only — no live model call)."""

import pytest

langchain_core = pytest.importorskip("langchain_core")
quesen_sdk = pytest.importorskip("quesen_sdk")

from quesen_langchain import (
    QuesenReportTool,
    QuesenSimulateTool,
    QuesenValidateTool,
)


def test_tools_have_names_and_descriptions():
    for cls in (QuesenValidateTool, QuesenSimulateTool, QuesenReportTool):
        t = cls(base_url="http://x", api_key="k")
        assert t.name.startswith("quesen_")
        assert len(t.description) > 30
        # BaseTool guarantees args_schema is a Pydantic model.
        assert t.args_schema is not None


def test_validate_tool_accepts_signal_kwargs():
    t = QuesenValidateTool(base_url="http://x")
    # We don't invoke _run against a live server here; we just check argument
    # schema binds correctly. The full round-trip is covered by the sdk tests.
    schema = t.args_schema.model_json_schema()
    props = schema["properties"]
    for k in ("domain_age_days", "engagement_ratio", "scam_keyword_count"):
        assert k in props


def test_report_tool_requires_request_id_and_outcome():
    t = QuesenReportTool(base_url="http://x")
    required = set(t.args_schema.model_json_schema().get("required", []))
    assert {"request_id", "outcome"}.issubset(required)
