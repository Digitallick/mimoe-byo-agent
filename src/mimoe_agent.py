"""
Small ReAct-style agent: LangChain ChatOpenAI plus a manual tool loop against mimOE local API.

mimOE exposes an OpenAI-compatible HTTP API; only base_url and api_key change vs cloud OpenAI.
A manual loop avoids churn in LangChain's higher-level agent helpers and fits small local LLMs.
"""
from __future__ import annotations

import os
import re
import sys
from typing import Callable

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI


def _env(name: str, default: str) -> str:
    v = os.environ.get(name)
    return v if v is not None and v != "" else default


def _multiply(pair: str) -> str:
    left, _, right = pair.partition(",")
    return str(float(left.strip()) * float(right.strip()))


TOOLS: dict[str, Callable[[str], str]] = {
    "multiply": _multiply,
}


SYSTEM = """You are a careful assistant with one tool.

To multiply two numbers, output exactly these two lines (nothing after Action Input on that line):
Action: multiply
Action Input: 6,7

You will then receive a line starting with Observation: followed by the numeric result.
Repeat if needed. When you have the user-facing reply, end with:
Final Answer: <answer>

If you do not need a tool, reply with only:
Final Answer: <answer>
"""


def _extract_final_answer(text: str) -> str | None:
    m = re.search(r"Final Answer:\s*(.+)", text, re.IGNORECASE | re.DOTALL)
    if not m:
        return None
    return m.group(1).strip()


def _extract_action(text: str) -> tuple[str, str] | None:
    m = re.search(
        r"Action:\s*(\w+)\s*\n\s*Action Input:\s*(.+)",
        text,
        re.IGNORECASE | re.MULTILINE,
    )
    if not m:
        return None
    name = m.group(1).strip().lower()
    arg = m.group(2).strip()
    return name, arg


def run_agent(question: str, max_steps: int = 6) -> str:
    llm = ChatOpenAI(
        base_url=_env("MIMOE_OPENAI_BASE_URL", "http://localhost:8083/mimik-ai/openai/v1"),
        api_key=_env("MIMOE_API_KEY", "1234"),
        model=_env("MIMOE_MODEL", "smollm2-360m"),
        temperature=0.2,
    )
    messages: list = [SystemMessage(content=SYSTEM), HumanMessage(content=question)]

    for _ in range(max_steps):
        reply = llm.invoke(messages)
        text = reply.content if isinstance(reply.content, str) else str(reply.content)
        messages.append(AIMessage(content=text))

        final = _extract_final_answer(text)
        if final:
            return final

        action = _extract_action(text)
        if not action:
            return text.strip()

        name, arg = action
        tool = TOOLS.get(name)
        if tool is None:
            messages.append(
                HumanMessage(
                    content=f"Observation: unknown action {name!r}. Use multiply or Final Answer."
                )
            )
            continue

        try:
            obs = tool(arg)
        except Exception as exc:
            obs = f"error: {exc}"
        messages.append(HumanMessage(content=f"Observation: {obs}"))

    return "Agent stopped after max steps; last model reply was truncated in context."


def main() -> None:
    q = " ".join(sys.argv[1:]).strip() or "What is 6 times 7?"
    print(run_agent(q))


if __name__ == "__main__":
    main()
