from fastapi import FastAPI
import uvicorn
import os


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World!"}
