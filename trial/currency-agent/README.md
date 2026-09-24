# Currency agent (third-party, run as a black box)

The A2A project's own LangGraph currency-conversion sample,
`samples/python/agents/langgraph` from
https://github.com/a2aproject/a2a-samples at commit `6603ba3f` (2026-08-04),
copied here so it can be run beside the analyst. `UPSTREAM-README.md` is the
sample's own README, unchanged.

**It does not run at `a2a-sdk` 1.1.5 as published** (`ModuleNotFoundError: No
module named 'a2a.server.apps'`; it was written for the 0.3 API). `PORT.diff`
is the whole port: the server app is built from `create_agent_card_routes` and
`create_jsonrpc_routes`, the card lists a `supported_interfaces` entry instead
of a `url`, and the executor uses the 1.x names for parts, states, helpers and
errors. In `app/agent.py` (the LangGraph agent itself) one line changed: the
Frankfurter rate API moved to `api.frankfurter.dev/v1` and the old host now
answers with a redirect the sample's `httpx.get` does not follow.

Run:

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fill in API_KEY
python -m app          # serves on http://localhost:10000
```
