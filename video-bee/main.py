from fastapi import FastAPI
from routers import users, projects, videos, auth, pexels
from database.database import engine
from database.base import Base
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title='FastAPI JWT', openapi_url='/openapi.json', docs_url='/docs',
    description='fastapi jwt'
)

origins = [
    "*",
    "http://localhost:3000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def create_tables():
    Base.metadata.create_all(bind=engine)


def define_router():
    app.include_router(users.router)
    app.include_router(projects.router)
    app.include_router(videos.router)
    app.include_router(auth.router)
    app.include_router(pexels.router)
def start_application():
    create_tables()
    define_router()


start_application()
