from fastapi import FastAPI
from .routers import v1
from .config import settings


app = FastAPI(
    title="AEKI Bounding Boxer",
    description="AEKI Engineering bounding boxer API service."
)

app.include_router(
    v1.router,
    prefix=settings.API_V1_PREFIX,
    tags=["v1"]
)

app.include_router(
    v1.router,
    prefix=settings.API_LATERST_PREFIX,
    tags=["latest"]
)

@app.get("/", name="Index")
async def root():
    return {"message": "AEKI ENGINEERING | EST. 2022, GDAŃSK UNIVERSITY OF TECHNOLOGY"}
