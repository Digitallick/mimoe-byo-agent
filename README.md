# mimOE BYO Agent (LangChain)

This project is a minimal "Bring Your Own Framework" assignment using **LangChain** with mimOE's **local OpenAI-compatible API**.  
It includes:

- `src/raw_chat.py`: direct OpenAI SDK smoke test to local mimOE.
- `src/mimoe_agent.py`: small ReAct-style agent with a manual tool loop (`multiply`).

The solution runs entirely against local mimOE inference (not the public OpenAI API).

## Assignment Checklist

- [x] Install and run mimOE locally
- [x] Load a local model in mimOE Studio
- [x] Verify OpenAI-compatible API connectivity
- [x] Build and run a LangChain-based local agent
- [x] Validate end-to-end execution locally

## Prerequisites

1. Install mimOE Studio or mimOE SE from the mimik developer portal: <https://developer.mimik.com>
2. In mimOE Studio, open **Model View** and load a model (example: `smollm2-360m`).
3. Confirm API details in Studio (base URL, key, model id). Default values used by this repo are below.

## Default Environment Values

The app uses these defaults when environment variables are not set:

- `MIMOE_OPENAI_BASE_URL=http://localhost:8083/mimik-ai/openai/v1`
- `MIMOE_API_KEY=1234`
- `MIMOE_MODEL=smollm2-360m`

You can override by copying `.env.example` into your shell environment.

## Setup

Run from the project root:

```bash
cd /Users/biglittlemonster/mimoe-byo-agent
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Connectivity Check

Before running Python code, verify mimOE API is reachable:

```bash
curl -s "http://localhost:8083/mimik-ai/openai/v1/models" \
  -H "Authorization: Bearer 1234"
```

You can also test chat completions directly:

```bash
curl -X POST "http://localhost:8083/mimik-ai/openai/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer 1234" \
  -d '{
    "model": "smollm2-360m",
    "messages": [{"role":"user","content":"Hello"}]
  }'
```

## Run Locally

```bash
source .venv/bin/activate
python -m src.raw_chat "Hello"
python -m src.mimoe_agent "What is 6 times 7?"
```

Expected behavior:

- `raw_chat` returns a normal assistant response from mimOE.
- `mimoe_agent` returns `42` for the multiplication question.

## End-to-End Test Result

Validated locally with mimOE running:

- `python -m src.raw_chat "Hello"` -> successful response
- `python -m src.mimoe_agent "What is 6 times 7?"` -> `42`

## Design Notes

- mimOE is OpenAI-compatible, so LangChain `ChatOpenAI` works with only `base_url`, `api_key`, and `model`.
- A manual ReAct loop is used for predictable behavior on small local models:
  - Parse `Action` and `Action Input`
  - Execute local tool (`multiply`)
  - Return `Observation`
  - Finish with `Final Answer`

## Troubleshooting

- **Connection refused on port 8083**: mimOE is not running or model is not loaded.
- **`requirements.txt` not found / `No module named src`**: run commands from the project root.
- **Wrong model name**: set `MIMOE_MODEL` to a loaded model id from mimOE Studio.

## License

MIT
