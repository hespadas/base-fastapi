from fastapi import FastAPI
from app.api import user
app = FastAPI()


@app.get("/")
def read_root():
    return {"msg": "Run Forrest, Run!"}


app.include_router(user.router)