# Build the Smallest Possible A2A Agent

Companion code for the "Build the Smallest Possible A2A Agent" video of A2A
Explained: the analyst at its minimum, served behind its card.

`analyst.py` is the agent with no protocol at all: a model with one lookup
(`price_history`, daily closes over `yfinance`) that decides what to fetch and
writes a few sentences. It reports each lookup it decides on through `note()`.

`server.py` is the same analyst served over A2A, 54 lines. The card says who the
agent is and what it offers; the executor opens a task for each message, marks it
working, posts each of the analyst's notes as a working-status message, attaches
the brief as an artifact named `brief`, and completes the task. The SDK serves
the card at `/.well-known/agent-card.json` and the JSON-RPC endpoint at `/`.

`ask.py` is the client from video 04, unchanged; only the URL on the command line
differs.

## Run

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env                 # fill in LLM_API_KEY
python server.py                     # terminal 1: the analyst, on port 9999
```

```bash
curl http://127.0.0.1:9999/.well-known/agent-card.json      # terminal 2: the card
python ask.py http://127.0.0.1:9999 "How did Apple do over the last month?"
```

The card arrives, then the task: `completed`, with the brief as its artifact.
What happens while the task is working, and what the agent does when the period
is missing, are the next two videos.
