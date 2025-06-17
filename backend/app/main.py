from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.routes import users, experiences
from app.api.routes import auth

app = FastAPI()


@app.get("/")
def read_root():
    return {"msg": "Run Forrest, Run!"}


app.include_router(users.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
app.include_router(experiences.router, prefix="/api")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
