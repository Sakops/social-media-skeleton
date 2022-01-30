from typing import Optional, List
from fastapi import APIRouter, Depends, status, HTTPException, Response
from .. import models, schemas, oauth
from app.database import SessionLocal, engine, get_db
from sqlalchemy.orm import Session
from logging import raiseExceptions

router = APIRouter(
    prefix="/vote",
    tags=["votes"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), user_id: int = Depends(oauth.get_current_users)):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Post with this id does not exist")
    vote_query = db.query(models.Vote).filter(models.Vote.post_id ==
                                              vote.post_id, models.Vote.user_id == user_id.id)
    found_vote = vote_query.first()
    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"user {user_id} has already liked the post")
        new_vote = models.Vote(post_id=vote.post_id,
                               user_id=user_id.id)
        db.add(new_vote)
        db.commit()
        return {"msg": "liked post"}
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Vote doesn't exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"msg": "deleted like"}
