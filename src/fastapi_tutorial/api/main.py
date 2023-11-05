from fastapi import FastAPI
from .utils.result import result
from . import roll

app = FastAPI()
app.include_router(roll.router)

@app.get("/")
@result
def root() -> str:
    return "Hello, World!"
