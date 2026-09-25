# Trial captures

Real runs of the code in `trial/`, saved verbatim from stdout on 2026-09-24 (US
market open; every lookup ends at the last completed close, 2026-09-23). The
videos replay these; nothing is recorded live. Move each capture to
`../a2a-explained/videos/NN-slug/assets/captures/` once that video's folder exists.

## Provenance

| | |
|---|---|
| Code | `a2a-explained-code` commit `542cb63` |
| `a2a-sdk` | 1.1.5 (protocol 1.0), JSON-RPC binding over Starlette 1.7.0 + uvicorn 0.53.0 |
| `mcp` | 2.2.0 (video 09's bridge, stdio) |
| Python | 3.14.7 |
| Model | OpenRouter, `openai/gpt-6-luna-pro`, through the `openai` client, for every agent |
| Price data | `yfinance` 1.7.0, live on the day |
| Exchange rates | Frankfurter (`api.frankfurter.dev`), rate dated 2026-09-24 |
| Currency agent | `a2aproject/a2a-samples` commit `6603ba3f`, `samples/python/agents/langgraph`, ported to SDK 1.x (`trial/currency-agent/PORT.diff`) |

## Videos 05–07: the analyst

| File | What it shows |
|---|---|
| `01-02-stream.txt` | `stream.py` on "How did Apple do over the last month?": the task arrives `submitted`, then `working` twice (the second carries the lookup and its reason), then the `brief` artifact, then `completed`. |
| `02-poll.txt` | `poll.py` on the same question: the plain send returns the task at once (`returnImmediately`), then `GetTask` sees `submitted` → `working` → `completed` and the artifact. |
| `03-04-chat.txt` | `chat.py "How did Apple do?" "the last month"`: the task stops in `input_required` with the analyst's question (no model call); the reply goes back on the same task and context ids and the task completes. |
| `03-clarification.txt` | `ask.py` on the same question: card, task id, `input_required`, the question. |
| `06-stream-comparison.txt` | Video 06's run. `stream.py` on "How did Apple do over the last month, and was that just the market?": the analyst fetches AAPL, then decides on its own to fetch SPY, with its reason, and the brief answers the comparison. |
| `06-poll-comparison.txt` | The same question through `poll.py`. |
| `01-judgement.txt` | The same judgement on another ticker: Nvidia over three months, with SPY fetched for the comparison. |

## Video 08: the wire

| File | What it shows |
|---|---|
| `../wire.log` | The raw wire, captured by `tap.py` sitting on port 9999 with the analyst behind it, driven by `wire.py`: the `GET` for the card and its JSON; a `POST /` carrying `A2A-Version: 1.0` and the JSON-RPC `SendMessage`, answered by a completed Task; `GetTask`; then `SendStreamingMessage` answered as `text/event-stream`, chunked, each `data:` line one event (task, two working updates, the artifact, completed), down to the closing `0` chunk. JSON is unfolded for reading; everything else is as it crossed. |
| `08-wire-brief.txt`, `08-wire-clarification.txt` | `wire.py`'s own output, SDK-decoded events, kept only as a cross-check; not a wire capture. |

## Video 09: the lookup behind MCP

| File | What it shows |
|---|---|
| `09-mcp-bridge.txt` | The analyst served with `ANALYST=analyst_mcp`, its lookup now `mcp_server.py` over stdio. The card is byte-for-byte the same, `ask.py` (video 04's client, unchanged) gets the same task shape and brief, and the streamed comparison shows the same two lookups arriving through MCP. |

## Video 10: the briefing agent

| File | What it shows |
|---|---|
| `10-briefing.txt` | `briefing.py` on "Summarize Apple's performance over the last month, and express the price change in euros.": both cards read; the analyst handed the summary (its brief gives the start and end closes and the $27.12 change); the currency agent handed the conversion; the assembled briefing states the euro amount and the exchange-rate date. |

## Video 12: the task outlives the call

| File | What it shows |
|---|---|
| `12-reconnect-during.txt` | `reconnect.py … 3`: the client hangs up after the first `working` event; three seconds later it is back, `GetTask` says `working`, so it subscribes: the subscription replays the current state, then delivers the artifact and `completed`; `GetTask` returns the brief. |
| `12-reconnect-after.txt` | `reconnect.py … 45`: back after the task finished; `GetTask` says `completed` and the brief is already in the task; no subscription. |
| `05b-webhook.txt` | `webhook.py`: a push-notification config goes with the send; the client hangs up; the server POSTs each event to the webhook with the `X-A2A-Notification-Token` header. |

## Videos 04 and 10: the currency agent

| File | What it shows |
|---|---|
| `currency-01-convert.txt` | `ask.py` on "How much is 100 US dollars in euros?": the sample creates a Task and completes it with a `conversion_result` artifact. |
| `currency-02-ask-back.txt` | `chat.py` on "How much is 100 dollars?" then "in euros": `input_required` asking for the currency, resumed on the same task and context, completed. |
