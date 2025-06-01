from fastapi import FastAPI
from app.api.routes import users
from app.api.routes import auth

app = FastAPI()


@app.get("/")
def read_root():
    return {"msg": "Run Forrest, Run!"}


app.include_router(users.router)
app.include_router(auth.router)
