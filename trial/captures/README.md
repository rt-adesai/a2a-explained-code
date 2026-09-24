# Trial captures

Real runs of the code in `trial/`, saved verbatim from stdout. The videos replay
these; nothing is recorded live. Move each capture to
`../a2a-explained/videos/NN-slug/assets/captures/` once that video's folder exists.

## Provenance

| | |
|---|---|
| Code | `a2a-explained-code` commit `65f00ff` (2026-09-24) |
| `a2a-sdk` | 1.1.5 (protocol 1.0), JSON-RPC binding, Starlette + uvicorn 0.53.0 |
| Python | 3.14.7 |
| Model | OpenRouter `anthropic/claude-sonnet-5` for the runs that call the model |
| Currency agent | `a2aproject/a2a-samples` commit `6603ba3f`, `samples/python/agents/langgraph`, ported to SDK 1.x (`trial/currency-agent/PORT.diff`) |

## Captures

| File | Run | Needs the model |
|---|---|---|
| `03-clarification.txt` | Run 3: `ask.py "How did Apple do?"` stops in `input_required` with the analyst's question; no model call was made | no |
| `08-wire-clarification.txt` | The same exchange on the wire: `GET /.well-known/agent-card.json`, the `SendStreamingMessage` JSON-RPC request with `A2A-Version: 1.0`, the SSE events (task `TASK_STATE_SUBMITTED`, then the `TASK_STATE_INPUT_REQUIRED` status update), and a `GetTask` request | no |
