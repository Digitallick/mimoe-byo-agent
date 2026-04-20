"""Minimal OpenAI SDK chat against mimOE (no LangChain). Useful sanity check."""
from __future__ import annotations

import os
import sys

from openai import OpenAI


def main() -> None:
    base = os.environ.get("MIMOE_OPENAI_BASE_URL", "http://localhost:8083/mimik-ai/openai/v1")
    key = os.environ.get("MIMOE_API_KEY", "1234")
    model = os.environ.get("MIMOE_MODEL", "smollm2-360m")
    prompt = " ".join(sys.argv[1:]).strip() or "Say hello in one short sentence."

    client = OpenAI(base_url=base, api_key=key)
    r = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    print(r.choices[0].message.content)


if __name__ == "__main__":
    main()
