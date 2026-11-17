"""Track 3 air threat advisor — minimal skeleton. Implement your advisor here.

See README.md for the full contract (endpoints, response shape, citations).
"""

import os
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

# Chat models a request may ask for in its optional `model` field. Both required
# models must stay in this set; add others if you support them.
SUPPORTED_MODELS = {
    "CSCS-Inference/google/gemma-4-31B-it",
    "RCP-AIaaS/swiss-ai/Apertus-large",
}
if MODEL:
    SUPPORTED_MODELS.add(MODEL)


class ModelNotAvailable(Exception):
    pass


@app.exception_handler(ModelNotAvailable)
def model_not_available(request: Request, exc: ModelNotAvailable) -> JSONResponse:
    return JSONResponse(status_code=400, content={"error": "model not available"})


def pick_model(requested: str | None) -> str:
    """The chat model for this request: the requested one, else the MODEL default.
    Never falls back silently: an unsupported model is a 400."""
    model = requested or MODEL
    if model not in SUPPORTED_MODELS:
        raise ModelNotAvailable()
    return model


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
