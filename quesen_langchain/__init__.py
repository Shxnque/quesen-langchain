"""Quesen LangChain integration — official BaseTool wrappers on top of quesen-sdk.

Includes the Agent Firewall tool (TSC v2), the legacy A2A risk tools, and
(v0.4.0) the fail-closed enforcement decorator `quesen_guard`.
"""

from .tool import (
    QuesenFirewallTool,
    QuesenReportTool,
    QuesenSimulateTool,
    QuesenValidateTool,
)
from .guard import quesen_guard

__version__ = "0.5.1"

__all__ = [
    "__version__",
    "QuesenFirewallTool",
    "QuesenValidateTool",
    "QuesenSimulateTool",
    "QuesenReportTool",
    "quesen_guard",
]
