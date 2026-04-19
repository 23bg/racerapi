from fastapi import FastAPI
from core.config import settings

app = FastAPI(title="hello", version="0.1.0")


@app.get("/")
def read_root():
    return {"message": "Welcome to hello"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
