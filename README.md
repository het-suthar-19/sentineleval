# SentinelEval

A multi-agent system that automatically red-teams and evaluates AI chatbots. Instead of manually writing test cases to check if a chatbot leaks information or gets manipulated, SentinelEval generates adversarial prompts itself, runs them against a target chatbot, scores the responses using two independent judges, and shows the results in a simple dashboard.

## Why this exists

As companies add AI agents into customer support, internal tools, and other workflows, a recurring question comes up: how do you know if the agent is safe to deploy. Most teams either skip testing entirely or write a handful of test cases by hand. This project automates that process using a small team of agents that each handle one part of the job, which mirrors how evaluation pipelines are actually built in production systems.

## How it works

The system has four roles, each handled by a separate agent or module:

1. **Attacker agent** generates adversarial prompts aimed at a chatbot, things like prompt injection attempts, requests to reveal internal instructions, or manipulative edge cases.
2. **Target agent** is the chatbot being tested. It responds to each adversarial prompt the way a real customer support bot would.
3. **Scorer agent** acts as a judge, deciding whether the target's response leaked information, got manipulated, or held its ground.
4. **DeepEval metric** runs as a second, independent judge using a different evaluation framework, so every response gets two separate opinions instead of relying on a single score.

All results are saved and shown in a Streamlit dashboard, where you can also trigger a new evaluation run and customize the target chatbot's system prompt directly from the browser.

## Architecture

```
Attacker Agent  --generates-->  Adversarial Test Cases
                                       |
                                       v
                              Target Agent (chatbot)
                                       |
                                       v
                    Scorer Agent  +  DeepEval GEval
                       (two independent judgments)
                                       |
                                       v
                         results/eval_results.json
                                       |
                                       v
                          Streamlit Dashboard (GUI)
```

## Tech used

- AutoGen-style multi-agent pattern (separate agent per role)
- Groq API for fast, free LLM inference (used by every agent, including a custom wrapper so DeepEval can run on Groq instead of requiring a separate OpenAI key)
- DeepEval for the second evaluation layer
- Streamlit for the dashboard and to run evaluations without using the command line
- Python, dotenv for configuration

## Running it locally

1. Clone the repo and create a virtual environment
   ```
   git clone https://github.com/het-suthar-19/sentineleval.git
   cd sentineleval
   python -m venv venv
   venv\Scripts\activate
   ```
2. Install dependencies
   ```
   pip install -r requirements.txt
   ```
3. Add your Groq API key in a `.env` file
   ```
   GROQ_API_KEY=your_key_here
   ```
4. Launch the dashboard
   ```
   streamlit run dashboard/app.py
   ```
5. Set the number of test cases, optionally customize the target chatbot's system prompt, and click run.

## What I learned building this

This was my first project combining multiple LLM calls into a coordinated pipeline rather than a single prompt. The most useful lessons were around reliability: LLMs do not reliably return clean JSON even when asked to, so every agent that needs structured output uses a stricter prompt plus a regex extraction step as a safety net. I also learned that automated judges, including DeepEval, can disagree with each other and sometimes with a human's own read of a response, which is part of why the project intentionally uses two separate scoring methods instead of trusting one.

## Possible extensions

- Point the target agent at a different chatbot backend (e.g. a locally running open source model) to test a system other than the project's own demo chatbot
- Add more adversarial categories beyond prompt injection, such as bias or factual consistency checks
- Export the results report as a PDF for sharing with a non-technical audience

## Screenshot

![Dashboard screenshot](./demo.png)
