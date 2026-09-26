# Implementation trial

The one running example of *A2A Explained*, built before any video is
storyboarded, plus the client scripts for the five required runs. Captures of
the real runs, with provenance, live in `captures/`. This folder is reshaped
into per-video folders as each video is authored: **04 and 05 have moved out**
(`../04-first-agent/`, `../05-analyst/`); what is here stays as the trial left it,
and `ask.py`, `analyst.py` and the currency agent are the copies those folders
started from.

| File | What it is |
|---|---|
| `analyst.py` | The analyst: a model with one lookup (`price_history` over `yfinance`) that decides what to fetch and writes a short brief |
| `server.py` | The same analyst served over A2A: card, executor, deterministic period check, task events; `python server.py` on port 9999 |
| `ask.py` | Video 04's client: read a card, send one message, print the task's state and artifact |
| `poll.py` | Video 06, first half: send, get the task back at once, poll `GetTask` until done |
| `stream.py` | Video 06, second half: the streaming send, events printed as they arrive |
| `chat.py` | Video 07: ask with no period, get asked back, answer on the same task (takes the agent URL, so it works on the currency agent too) |
| `reconnect.py` | Video 12: hang up mid-task, come back, `GetTask`, and `SubscribeToTask` only if the task is still active |
| `webhook.py` | Video 12, option B: register a push-notification webhook, hang up, receive the brief there |
| `wire.py` | A driver that makes the three calls video 08 reads: the plain send, `GetTask`, the streaming send (its own output is SDK-decoded, not the wire) |
| `tap.py` | Video 08: the wiretap; takes port 9999, runs the analyst behind it, copies every byte both ways into `wire.log` |
| `mcp_server.py` | Video 09: the analyst's lookup as an MCP server, line for line the pattern of MCP Explained's stock server |
| `analyst_mcp.py` | Video 09: the analyst with its lookup behind MCP; `ANALYST=analyst_mcp python server.py` serves it, A2A side unchanged |
| `briefing.py` | Video 10: a briefing agent with two cards on its list, one client per card, the cards' skills as the model's menu |
| `currency-agent/` | The third-party agent for videos 04 and 10 (the A2A project's LangGraph currency sample) |

Setup, as in `mcp-explained-code`:

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env    # fill in LLM_API_KEY
python server.py        # terminal 1
python ask.py http://127.0.0.1:9999 "How did Apple do over the last month?"   # terminal 2
```
