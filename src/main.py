from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import (
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.responses import JSONResponse

from src.exceptions import WeightsNotFound
from .routers import v1
from .config import settings

description = """
<center><img src="/static/aeki-chair.png" width="25%" height="25%" /></center>

---

<center>**[Browse GitHub Code Repository](https://github.com/AEKI-Engineering/API-service) | [Check latest model runs](https://wandb.ai/aeki-engineering)**</center>

---

**AEKI Engineering Bounding Boxer API Service.**

**EST. 2022, GDAŃSK UNIVERSITY OF TECHNOLOGY**

# Routes
"""


app = FastAPI(
    title="AEKI Bounding Boxer",
    description=description,
    version=settings.APP_VERSION,
    docs_url=None,
    redoc_url=None,
    openapi_tags=[
        {"name": "latest", "description": "Uses latest version of the API."},
        {"name": "v1", "description": "Uses version 1 of the API."},
    ]
)

app.include_router(
    v1.router,
    prefix=settings.API_LATERST_PREFIX,
    tags=["latest"]
)

app.include_router(
    v1.router,
    prefix=settings.API_V1_PREFIX,
    tags=["v1"]
)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - docs",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_css_url="/static/swagger-ui.css",
        swagger_favicon_url="/static/aeki-chair-white.png"
    )

@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()

@app.exception_handler(WeightsNotFound)
async def weights_not_found_handler(request: Request, exc: WeightsNotFound):
    return JSONResponse(status_code=503, content={"message": str(exc)})

@app.get("/", name="Index", description="Returns name of the API.")
async def root():
    return {"message": "AEKI ENGINEERING | EST. 2022, GDANSK UNIVERSITY OF TECHNOLOGY"}
