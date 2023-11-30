from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from app.middlewares import add_process_time_header
from . import models, database
from .routes import tasks, users, login, user_groups


# Now Alembic handle this
# models.Base.metadata.create_all(bind=database.engine)


app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(BaseHTTPMiddleware, dispatch=add_process_time_header)


# routes

@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(users.router)
app.include_router(login.router)
app.include_router(tasks.router)
app.include_router(user_groups.router)
