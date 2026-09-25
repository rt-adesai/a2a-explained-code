# A2A Explained — companion code

Runnable code for the **A2A Explained** video series, the sequel to
[MCP Explained](https://github.com/rt-adesai/mcp-explained-code). Every video that
shows code will have its code here in full, in the exact form that video shows it:
clone the repo, `cd` into the video's folder, and run it.

The series follows one running example, **the analyst**: a stock brief agent served
over the Agent2Agent protocol with the Python `a2a-sdk`. Ask it about a ticker over
a period and it fetches the price history, decides what is worth saying, and returns
a short brief as an artifact. Asked without a period, it asks back. The videos also
talk to an agent we did not write, the A2A project's currency-conversion sample,
run locally.

## Status

The series is being planned, and this repo holds its **implementation trial**:
the analyst built and proven before any video is storyboarded, with the real
exchanges captured for the videos to replay.

| Folder | What it holds |
|---|---|
| [`trial/`](./trial/) | The analyst (`analyst.py`, `server.py`), one client script per video moment (`ask.py`, `poll.py`, `stream.py`, `chat.py`, `reconnect.py`, `webhook.py`, `wire.py`), the currency agent ported to the pinned SDK, and `captures/` with every run and its provenance |

Video folders (`05-analyst/`, `06-analyst/`, …) will be carved out of `trial/` as
each video is authored, following the convention MCP Explained settled on: one
runnable folder per video state, named for the video, two videos sharing a folder
only where the code between them is identical.

## Setup pattern (all folders)

Every folder reads its configuration from a local `.env` file (never committed).
Copy the folder's `.env.example` to `.env`, fill in your key, then:

```bash
cd <folder>
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

The model is any OpenAI-compatible endpoint (`LLM_BASE_URL`, `LLM_MODEL`,
`LLM_API_KEY`); the examples default to OpenRouter. Dependencies are pinned
exactly, because the repo promises the environment each video was captured in.
The A2A SDK is `a2a-sdk` 1.1.5, which implements spec v1.0.

## Try the analyst

```bash
cd trial
python server.py                                   # terminal 1: the analyst, on port 9999
python ask.py http://127.0.0.1:9999 "How did Apple do over the last month?"   # terminal 2
python stream.py "How did Apple do over the last month, and was that just the market?"
python chat.py http://127.0.0.1:9999 "How did Apple do?" "the last month"
```

The first prints the card, the task and its brief. The second streams the task's
life, including the analyst deciding to fetch a market benchmark. The third stops
in `input-required`, answers the question, and completes the same task.
