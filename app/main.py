from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import SessionLocal, engine
from .routers import posts, users, login, vote
from .config import settings
from app import database


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

my_posts = [{"title": "title of post 1",
             "content": "content of post 1", "id": 3}, {"title": "favourite foods", "content": "i like pizza", "id": 1}]


# def find_post(id):
#     for post in my_posts:
#         if post["id"] == id:
#             return post


# def find_index_post(id):
#     for index, p in enumerate(my_posts):
#         if p['id'] == id:
#             return index

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(login.router)
app.include_router(vote.router)


@app.get("/")
async def root():
    return {"message": "Welcome to my api here"}
