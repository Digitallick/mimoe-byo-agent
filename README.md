# mimOE BYO Agent (LangChain)

This is a small assignment project that runs a local agent on top of mimOE's OpenAI-compatible API.
It includes a direct chat smoke test and a simple LangChain ReAct-style agent with one tool (`multiply`).

## Prerequisites

1. Install mimOE from <https://developer.mimik.com>.
2. Load a model in mimOE Studio (example: `smollm2-360m`).
3. Make sure the local API is running.

Default values used by this project:

- `MIMOE_OPENAI_BASE_URL=http://localhost:8083/mimik-ai/openai/v1`
- `MIMOE_API_KEY=1234`
- `MIMOE_MODEL=smollm2-360m`

## Setup

```bash
cd /Users/biglittlemonster/mimoe-byo-agent
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Run

```bash
source .venv/bin/activate
python -m src.raw_chat "Hello"
python -m src.mimoe_agent "What is 6 times 7?"
```

## Quick Verification

After mimOE is up, both commands should complete without errors. Exact wording can vary by model; you should see a normal reply from `raw_chat` and a correct multiply result from `mimoe_agent` (often `42` or a line that includes it).

## Repository

<https://github.com/Digitallick/mimoe-byo-agent>

## License

MIT — a common permissive open-source license: others may use, modify, and redistribute the code with few restrictions, as long as the license notice is preserved. Full text: <https://opensource.org/licenses/MIT>
