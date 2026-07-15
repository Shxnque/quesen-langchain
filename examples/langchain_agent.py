"""5-minute LangChain integration — gated by Quesen risk verdict."""

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI  # pip install langchain-openai

from quesen_langchain import QuesenReportTool, QuesenValidateTool


def main() -> None:
    validate = QuesenValidateTool(base_url="https://<your-quesen>", api_key="sk_live_abc")
    report = QuesenReportTool(base_url="https://<your-quesen>", api_key="sk_live_abc")

    agent = ChatOpenAI(model="gpt-4o-mini").bind_tools([validate, report])
    prompt = [
        SystemMessage(content=(
            "You are a defensive DeFi agent. BEFORE taking any action, you MUST call "
            "quesen_validate with domain_age_days, engagement_ratio, scam_keyword_count. "
            "Do NOT proceed unless the decision is PROCEED."
        )),
        HumanMessage(content=(
            "An X post says a new token launched 1 day ago has 4 scam keywords in the "
            "caption and 95% engagement rate. Should I ape in?"
        )),
    ]
    print(agent.invoke(prompt))


if __name__ == "__main__":
    main()
