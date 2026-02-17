from typing import Any

import asyncio
import httpx

from fastapi import FastAPI, Request, status
from fastapi.responses import Response
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager

class KeepAlive:
    _url: str
    _period_sec: float
    _task: asyncio.Task[Any] | None

    def __init__(self, url: str, period_sec: float=300):
        self._url = url
        self._period_sec = period_sec
        self._task = None

    def start(self):
        if self._task is None:
            self._task = asyncio.create_task(self._run())

    async def _run(self):
        async with httpx.AsyncClient() as client:
            while True:
                await asyncio.sleep(self._period_sec)

                try:
                    await client.get(self._url, timeout=5)
                except Exception:
                    pass

    def stop(self):
        if self._task is None:
            return
        
        self._task.cancel()


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.keep_alive = None
    yield
    if app.state.keep_alive is not None:
        app.state.keep_alive.stop()

app = FastAPI(lifespan=lifespan)

templates = Jinja2Templates(directory="templates")

@app.get("/")
async def root(request: Request):
    url = f"{request.url.scheme}://{request.url.netloc}/ping"

    if app.state.keep_alive is None:
        app.state.keep_alive = KeepAlive(url, 15)
        app.state.keep_alive.start()

    return templates.TemplateResponse(
        request=request, name="Index.html.j2", context={"url": url}
    )

@app.get("/ping")
async def ping():
    return Response(status_code=status.HTTP_204_NO_CONTENT)