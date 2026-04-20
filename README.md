# mimOE BYO Agent (LangChain)

Small **BYO framework** demo: LangChain `ChatOpenAI` pointed at mimOE’s **local OpenAI-compatible** inference (not cloud OpenAI).  
`src/raw_chat.py` is a minimal OpenAI SDK sanity check; `src/mimoe_agent.py` is a tiny ReAct-style loop with one tool (`multiply`) so behavior stays easy to reason about on a small local model.

## Prerequisites (per Mimik exercise)

1. Install **mimOE Studio** from the early access page: <https://developer.mimik.com/mimOE-studio-early-access-download-v2> (overview: <https://developer.mimik.com>).
2. Open **Model View**, pick a bundled model such as **SmolLM2** (`smollm2-360m`), and load it.
3. In Model View, open **API** and note the local base URL, bearer token, and model id (defaults below match typical Studio setup).
4. Keep the local inference service running while you run the Python commands below.

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
