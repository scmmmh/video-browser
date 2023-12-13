"""The FastAPI frontend server."""
import logging

from copy import deepcopy
from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from uvicorn.config import LOGGING_CONFIG

from video_browser.backend import api


logging_config = deepcopy(LOGGING_CONFIG)
logging_config['loggers']['video_browser'] = {
    'level': 'DEBUG',
    'qualname': 'video_browser',
    'handlers': ['default'],
}
logging_config['formatters']['default']['fmt'] = '%(levelprefix)s %(name)-40s %(message)s'
logging.config.dictConfig(logging_config)

app = FastAPI()
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.mount("/ui", StaticFiles(packages=[("video_browser.backend", "ui/dist")], html=True))
app.include_router(api.router)


@app.get('/', response_class=RedirectResponse)
def redirect_to_ui() -> str:
    """Redirect to the UI."""
    return '/ui'
