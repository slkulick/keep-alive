# Keep Alive

A [FastAPI](https://fastapi.tiangolo.com/) app demonstrating a simple keep-alive mechanism preventing the server from being shutdown due to inactivity. Useful when deploying to [Render.com](https://render.com/).

## Details

The free tier of [Render.com](https://render.com/) shuts down your server after about 15 minutes of inactivity. To prevent this, the app pings itself (does an GET request to "/") every five minutes.

## Setup

```
uv sync --locked
```

## Run locally

```
uv run uvicorn main:app --port 8080
```