from fastapi import FastAPI
from app.api.routes import users, experiences
from app.api.routes import auth

app = FastAPI()


@app.get("/")
def read_root():
    return {"msg": "Run Forrest, Run!"}


app.include_router(users.router)
app.include_router(auth.router)
app.include_router(experiences.router)
