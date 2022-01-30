from fastapi import Depends, FastAPI, Response, status, HTTPException, APIRouter
from typing import Optional, List
from .. import models, schemas
from app.database import SessionLocal, engine, get_db
from sqlalchemy.orm import Session
from logging import raiseExceptions
from .. import utils

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

# creating users


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserInfo)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # hashing passwords
    hashed = utils.hash(user.password)
    user.password = hashed
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

# get 1 user


@router.get("/{id}", response_model=schemas.UserInfo)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id of '{id}' not found")
    db.commit()
    print(user)
    return user

# get all users


@router.get("/", response_model=List[schemas.UserInfo])
def get_posts(db: Session = Depends(get_db)):

    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    users = db.query(models.User).all()
    return users

# delete user


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db)):
    delete_user = db.query(models.User).filter(models.User.id == id)
    if delete_user == None:
        raiseExceptions(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"user with id of '{id}' not found")
    delete_user.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
