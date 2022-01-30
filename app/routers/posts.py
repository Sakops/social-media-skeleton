from fastapi import Depends, FastAPI, Response, status, HTTPException, APIRouter
from typing import Optional, List
from .. import models, schemas, oauth
from app.database import SessionLocal, engine, get_db
from sqlalchemy.orm import Session
from sqlalchemy import func
from logging import raiseExceptions

router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)


@router.get("/")
def get_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    print(limit)
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    # posts = db.query(models.Post).filter(models.Post.title.contains(
    #     search)).limit(limit).offset(skip).all()
    # sqlalchemy join
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("Votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(
            search)).limit(limit).offset(skip).all()
    return posts


@ router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), user_id: int = Depends(oauth.get_current_users)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES(%s, %s, %s) RETURNING *""",
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(poster_id=user_id.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# title str, content str

# get single post


@ router.get("/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    # post = cursor.fetchone()
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("Votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id of '{id}' not found")
    db.commit()
    return post
# deleting


@ router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,  db: Session = Depends(get_db), user_id: int = Depends(oauth.get_current_users)):
    # cursor.execute(
    #     """DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    # delete_post = cursor.fetchone()
    # conn.commit()
    delete_post = db.query(models.Post).filter(models.Post.id == id)

    post = delete_post.first()

    if post == None:
        raiseExceptions(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post with id of '{id}' not found")
    if post.poster_id != user_id.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="not authorized")
    else:
        delete_post.delete(synchronize_session=False)

    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# updating


@router.put("/{id}", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), user_id: int = Depends(oauth.get_current_users)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #                (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raiseExceptions(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post with id of '{id}' not found")
    if post.poster_id != user_id.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="unauthorized action")
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
