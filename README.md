# Track 3 — application template

Starter skeleton for the Track 3 air threat advisor. Read the scenario, the data
description, the full I/O contract and the submission rules on the website:
<https://hackathon-armasuisse.github.io/tracks/track-3/>

This template uses FastAPI and Uvicorn as a simple starting point, for more information see this [description](https://www.geeksforgeeks.org/python/fastapi-uvicorn/). We note that usage of this template is **optional**. You can start from scratch or use your own framework, as long as you meet the requirements.

## What's here

- `app/main.py` — the `/advise` and `/message` endpoint skeletons; implement your
  advisor here.
- `inference.env.example` — the inference endpoint variables we pass at deploy.
- `Dockerfile` — builds and runs the app on port 8080.
- `compose.yaml` — runs the app behind a TLS-terminating reverse proxy.
- `Caddyfile` — the reverse proxy configuration, replace `N` with your team number.

The siren record and the monitoring feed are distributed separately as an encrypted zip (see the website).

## Deploying on your team VM

Your VM already has a TLS certificate and a public hostname,
`llmhack-team-N.hackathon.intlab.ch`. `compose.yaml` in this repository runs two
containers: **Caddy**, which terminates TLS on that hostname, and **your app**,
which Caddy reaches at `app:8080` on the internal network. Before starting to build, do the following two steps:

1. Copy `inference.env.example` to `inference.env` and fill in the values for your team.
2. In the `Caddyfile`, replace `N` with your team number.
