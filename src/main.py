from fastapi import FastAPI
import uvicorn
import os

# load environment variables
port = os.environ["PORT"]

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World!"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
