# Talk to Your First Agent

Companion code for the "Talk to Your First Agent" video of A2A Explained: our own
client talking to an agent we did not write.

`ask.py` is the whole client, 36 lines and no model of its own. It reads the
agent's card from its well-known address, sends one message, and prints what
comes back: the task's id, its state, anything the agent says, and its artifacts.
It is the client every later video reuses; pointing it at a different agent is a
matter of changing the URL on the command line.

`currency-agent/` is the agent on the other end, treated as a black box: the A2A
project's own currency-conversion sample, run locally. Its README says what it is
and the one thing we had to do to run it at our SDK pin. The video shows its card
and its output, never its code.

## Run

The client needs no key. The currency agent needs a model; give it one in its
own `.env` (any OpenAI-compatible endpoint):

```bash
cd currency-agent
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env                 # fill in API_KEY
python -m app                        # terminal 1: the currency agent, on port 10000
```

Then, from this folder, in a second terminal:

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python ask.py http://localhost:10000 "How much is 100 US dollars in euros?"
```

The card arrives first (name, description, skills), then the task: created by the
agent for our message, `completed`, with a `conversion_result` artifact holding
the answer.

Ask without a currency and the same client shows the task stopping instead:

```bash
python ask.py http://localhost:10000 "How much is 100 dollars?"
```

The task ends `input_required`, and the agent's question is on it. Answering on
the same task is what video 07 builds.
