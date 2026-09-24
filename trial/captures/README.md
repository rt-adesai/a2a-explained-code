# Trial captures

Real runs of the code in `trial/`, saved verbatim from stdout on 2026-09-24. The
videos replay these; nothing is recorded live. Move each capture to
`../a2a-explained/videos/NN-slug/assets/captures/` once that video's folder exists.

## Provenance

| | |
|---|---|
| Code | `a2a-explained-code` commit `0178c3c` |
| `a2a-sdk` | 1.1.5 (protocol 1.0), JSON-RPC binding over Starlette 1.7.0 + uvicorn 0.53.0 |
| Python | 3.14.7 |
| Model | OpenRouter, `openai/gpt-6-luna-pro`, through the `openai` client |
| Price data | `yfinance` 1.7.0, live on the day |
| Currency agent | `a2aproject/a2a-samples` commit `6603ba3f`, `samples/python/agents/langgraph`, ported to SDK 1.x (`trial/currency-agent/PORT.diff`), same model |

## The five required runs

| File | Run | What it shows |
|---|---|---|
| `01-02-stream.txt` | 1 and 2 (streaming) | `stream.py`: one genuine brief on Apple over the last month. The task arrives `submitted`, then `working` twice (the second carries the analyst's lookup and its reason), then the `brief` artifact, then `completed`. |
| `06-stream-comparison.txt` | 1 and 2 (video 06's run) | `stream.py` on "How did Apple do over the last month, and was that just the market?": the analyst fetches AAPL, then decides on its own to fetch SPY ("Compare Apple with the broad market over the same month"), and the brief answers the comparison. Two visible choices, one artifact. |
| `06-poll-comparison.txt` | 2 (video 06's run, polling) | `poll.py` on the same question: `submitted` → `working` → `completed` by `GetTask`, then the artifact. |
| `01-judgement.txt` | 1 (judgement, other ticker) | `stream.py` on "How did Nvidia do over the last three months, and was that just the market?": the analyst fetches NVDA, then decides on its own to fetch SPY to answer the comparison, and the brief says so. |
| `02-poll.txt` | 2 (polling) | `poll.py`: the plain send returns the task at once (`returnImmediately`), then `GetTask` sees `submitted` → `working` → `completed` and the artifact. |
| `03-04-chat.txt` | 3 and 4 | `chat.py "How did Apple do?" "the last month"`: the task stops in `input_required` with the analyst's question (no model call); the reply goes back on the same task and context ids and the task completes. |
| `03-clarification.txt` | 3 (video 04's client) | `ask.py` on the same question: card, task id, `input_required`, the question. |
| `05a-reconnect.txt` | 5, option A | `reconnect.py`: the client hangs up after the first `working` event; the server keeps going; the client comes back, `SubscribeToTask` replays the current state and delivers the artifact and `completed`; `GetTask` returns the brief. |
| `05b-webhook.txt` | 5, option B | `webhook.py`: a push-notification config goes with the send; the client hangs up; the server POSTs each event (task, working ×2, the artifact, completed) to the webhook with the `X-A2A-Notification-Token` header. |

## The wire (video 08)

| File | What it shows |
|---|---|
| `08-wire-brief.txt` | Every request `wire.py` sends for a full brief: `GET /.well-known/agent-card.json`; a JSON-RPC `SendMessage` (with `A2A-Version: 1.0`) answered by a completed Task; `GetTask`; then a `SendStreamingMessage` answered as `text/event-stream` with the task, two status updates, the artifact update and the completed status. |
| `08-wire-clarification.txt` | The same on a question with no period: the Task comes back `TASK_STATE_INPUT_REQUIRED` with the analyst's message. |

## The currency agent (videos 04 and 10)

| File | What it shows |
|---|---|
| `currency-01-convert.txt` | `ask.py` on "How much is 100 US dollars in euros?": the sample creates a Task (not a direct Message) and completes it with a `conversion_result` artifact. |
| `currency-02-ask-back.txt` | `chat.py` on "How much is 100 dollars?" then "in euros": the task stops in `input_required` asking for the currency, resumes on the same task and context, and completes. |
