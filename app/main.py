"""Track 3 air threat advisor — minimal skeleton. Implement your advisor here.

See README.md for the full contract (endpoints, response shape, citations).
"""

import json
import os
import time
import urllib.request
from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI(title="Track 3 air threat advisor")

CORPUS_DIR = os.environ.get("CORPUS_DIR", "/corpus")
SIRENS = os.path.join(CORPUS_DIR, "sirens.csv")
MESSAGES = os.path.join(CORPUS_DIR, "messages.csv")

# Inference endpoint (OpenAI-compatible) — see inference.env.example.
OPENAI_BASE_URL = os.environ.get("OPENAI_BASE_URL")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
MODEL = os.environ.get("MODEL")  # default chat model, used when a request has no `model`

# A request may ask for any model the inference endpoint serves, in its optional
# `model` field. We check it against the endpoint's /models list, cached for a
# few minutes so the check does not eat into your rate limit.
MODELS_TTL_SECONDS = 600
_models_cache: tuple[float, set[str]] = (0.0, set())


def available_models() -> set[str]:
    global _models_cache
    fetched_at, models = _models_cache
    if time.monotonic() - fetched_at < MODELS_TTL_SECONDS:
        return models
    try:
        req = urllib.request.Request(
            f"{OPENAI_BASE_URL.rstrip('/')}/models",
            headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            models = {m["id"] for m in json.load(resp)["data"]}
        _models_cache = (time.monotonic(), models)
    except Exception:
        pass  # endpoint unreachable: keep the last list we had
    return _models_cache[1]


class ModelNotAvailable(Exception):
    pass


@app.exception_handler(ModelNotAvailable)
def model_not_available(request: Request, exc: ModelNotAvailable) -> JSONResponse:
    return JSONResponse(status_code=400, content={"error": "model not available"})


def pick_model(requested: str | None) -> str:
    """The chat model for this request: the requested one, else the MODEL default.
    Never falls back silently: a model the endpoint does not serve is a 400."""
    if not requested or requested == MODEL:
        return MODEL
    if requested not in available_models():
        raise ModelNotAvailable()
    return requested


POSTED: list[dict[str, str]] = []


class Location(BaseModel):
    text: str | None = None      # free-form, e.g. "near the big airport east of Kyiv"
    place: str | None = None
    raion: str | None = None
    oblast: str | None = None


class AdviseRequest(BaseModel):
    query: str
    as_of: str                   # UTC, e.g. "2026-08-27T01:45"
    location: Location | None = None
    model: str | None = None     # optional: chat model for this request


class Message(BaseModel):
    text: str
    timestamp: str               # UTC


@app.post("/message", status_code=201)
def post_message(msg: Message) -> dict:
    # TODO: store the message so that later /advise calls see it.
    POSTED.append(msg.model_dump())
    return {"stored": True}


@app.post("/advise")
def advise(req: AdviseRequest) -> dict:
    model = pick_model(req.model)  # use this model for the chat completions
    # TODO: implement your advisor.

    return {
        "advice": "TODO: not implemented",
        "area": None,
        "siren_active": False,
        "citations": [],          # siren_ids only, e.g. ["S-02278"]
        "as_of": req.as_of,
        # "threat_level" is optional and the tiers are yours to design. If you
        # return it, document your scale in this README and apply it consistently.
    }


@app.get("/health")
def health() -> dict:
    return {"ok": True}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
