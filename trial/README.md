# Implementation trial

The one running example of *A2A Explained*, built before any video is
storyboarded, plus the client scripts for the five required runs. Captures of
the real runs, with provenance, live in `captures/`. This folder is reshaped
into per-video folders once the series plan settles.

| File | What it is |
|---|---|
| `analyst.py` | The analyst: a model with one lookup (`price_history` over `yfinance`) that decides what to fetch and writes a short brief |
| `server.py` | The same analyst served over A2A: card, executor, deterministic period check, task events; `python server.py` on port 9999 |
| `ask.py` | Video 04's client: read a card, send one message, print the task's state and artifact |
| `poll.py` | Video 06, first half: send, get the task back at once, poll `GetTask` until done |
| `stream.py` | Video 06, second half: the streaming send, events printed as they arrive |
| `chat.py` | Video 07: ask with no period, get asked back, answer on the same task |
| `reconnect.py` | Video 12, option A: hang up mid-task, come back, `SubscribeToTask` |
| `webhook.py` | Video 12, option B: register a push-notification webhook, hang up, receive the brief there |
| `wire.py` | Video 08: every request the client sends, and the frames that come back |
| `currency-agent/` | The third-party agent for videos 04 and 10 (the A2A project's LangGraph currency sample) |

Setup, as in `mcp-explained-code`:

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env    # fill in LLM_API_KEY
python server.py        # terminal 1
python ask.py http://127.0.0.1:9999 "How did Apple do over the last month?"   # terminal 2
```
