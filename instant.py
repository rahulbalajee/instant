from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from openai import OpenAI, APITimeoutError

app = FastAPI()

# Created once at import time and reused across requests, instead of
# rebuilding the client on every call (cheaper, like a package-level var in Go).
#
# timeout: give up on a single request after 10s instead of the SDK default of 600s.
# max_retries: how many times the SDK retries on transient failures (default is 2).
#   Note: the timeout applies *per attempt*, so worst-case wall time is roughly
#   timeout * (max_retries + 1). With 10s and 1 retry that's ~20s, not 10s.
client = OpenAI(timeout=10.0, max_retries=1)

BASE_PROMPT = """
You are on a website that has just been deployed to production for the first time!
Please reply with an enthusiastic announcement to welcome visitors to the site, explaining that it is live on production for the first time!
"""


@app.get("/", response_class=HTMLResponse)
async def instant(tone: str = "enthusiastic", language: str = "English", sentences: int = 3):
    # Each function argument above automatically becomes a query parameter.
    # Visiting /?tone=pirate&language=Spanish&sentences=5 fills these in.
    prompt = (
        f"{BASE_PROMPT}\n"
        f"Write the announcement in a {tone} tone, "
        f"in {language}, "
        f"in about {sentences} sentences."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-5-nano",
            messages=[{"role": "user", "content": prompt}],
        )
        reply = response.choices[0].message.content
        if reply is None:
            reply = "Welcome! (The model returned an empty response.)"
    except APITimeoutError:
        # The request exceeded the timeout above (after exhausting retries).
        # Caught before the broad handler so we can show a specific message.
        reply = "The announcement is taking longer than expected. Please refresh to try again."
    except Exception as err:
        # Anything else thrown above (network error, bad API key, etc.) lands here.
        # This is Python's version of Go's `if err != nil`, but caught rather than returned.
        reply = f"Sorry, something went wrong reaching the model: {err}"

    reply = reply.replace("\n", "<br/>")
    html = f"<html><head><title>Live in an Instant!</title></head><body><p>{reply}</p></body></html>"
    return HTMLResponse(content=html)
