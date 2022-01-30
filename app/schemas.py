from turtle import title
from dotenv import Optional
from pydantic import BaseModel, EmailStr, conint
from .database import Base
from datetime import datetime


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True  # default


class PostCreate(PostBase):
    pass


class UserInfo(BaseModel):
    id: int
    email: EmailStr
    create_at: datetime

    class Config:
        orm_mode = True


class Post(PostBase):
    id: int
    create_at: datetime
    poster_id: int
    post_owner: UserInfo

    class Config:
        orm_mode = True


class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


# login


class UserLogin(BaseModel):
    email: EmailStr
    password: str

# token


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str]

# vote


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)
