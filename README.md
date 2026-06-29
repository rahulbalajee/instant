# instant

A tiny [FastAPI](https://fastapi.tiangolo.com/) app that asks an OpenAI model to
generate an enthusiastic "we're live!" announcement, rendered as a minimal HTML page.
Designed to deploy to [Vercel](https://vercel.com/) out of the box.

## What it does

`GET /` returns an HTML page containing an AI-generated welcome message. The tone,
language, and length are controllable via query parameters:

| Parameter   | Default        | Example                          |
| ----------- | -------------- | -------------------------------- |
| `tone`      | `enthusiastic` | `?tone=pirate`                   |
| `language`  | `English`      | `?language=Spanish`              |
| `sentences` | `3`            | `?sentences=5`                   |

Example: `/?tone=pirate&language=Spanish&sentences=5`

## Requirements

- Python 3.9+
- An OpenAI API key in the environment as `OPENAI_API_KEY`

## Run locally

```bash
pip install -r requirements.txt
export OPENAI_API_KEY=sk-...
uvicorn instant:app --reload
```

Then open http://127.0.0.1:8000/

## Deploy to Vercel

The included `vercel.json` builds `instant.py` with the `@vercel/python` runtime and
routes all traffic to it. Set `OPENAI_API_KEY` in your Vercel project's environment
variables, then deploy:

```bash
vercel
```

## Notes

- The OpenAI client is created once at import time and reused across requests.
- Requests time out after 10s per attempt with 1 retry (worst case ~20s).
- Errors (timeout, bad key, network) are caught and shown as a friendly message
  rather than crashing the request.
