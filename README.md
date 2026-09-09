# Track 3 — application template

Starter skeleton for the Track 3 air threat advisor. Read the scenario, the data
description, the full I/O contract and the submission rules on the website:
<https://hackathon-armasuisse.github.io/tracks/track-3/>

We note that usage of this template is **optional**. You can start from scratch or use your own framework, as long as you meet the requirements.

## What's here

- `app/main.py` — the `/advise` and `/message` endpoint skeletons; implement your
  advisor here.
- `inference.env.example` — the inference endpoint variables we pass at deploy.
- `Dockerfile` — builds and runs the app on port 8080.

The siren record and the monitoring feed are distributed separately as an encrypted zip (see the website).

## Run

```bash
docker build -t track3 .
docker run -p 8080:8080 -v /path/to/track3_data:/corpus:ro --env-file inference.env track3
```



