from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def Root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
