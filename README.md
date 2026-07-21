# Quesen — LangChain / LangGraph Tool

> Deterministic A2A risk validation as a LangChain `BaseTool`. **Integrate in under 5 minutes.**

**Developer portal:** https://senueren.co.za/quesen · **Source:** https://github.com/Shxnque/quesen
**Doctrine:** governance and product decisions live in the parent repo's `DOCTRINE.md`. This package is a distribution channel.

---

## Install

```bash
pip install quesen-langchain
# or from source while we publish:
pip install git+https://github.com/Shxnque/quesen-langchain.git
```

Brings `quesen-sdk` and `langchain-core` with it. No LLM lock-in.

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

## What ships

| Tool | Wraps | Purpose |
|---|---|---|
| `QuesenValidateTool` | `POST /validate` | Deterministic PROCEED/REVIEW/SKIP verdict |
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

MIT license. See [`senueren.co.za/quesen`](https://senueren.co.za/quesen) for canonical documentation.
