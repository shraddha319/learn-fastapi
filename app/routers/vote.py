from fastapi import APIRouter, HTTPException, status, Depends
from .. import schemas, database, oauth2, models
from sqlalchemy.orm import Session

router = APIRouter(prefix='/vote', tags=['Vote'])

@router.post('/', status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), user: schemas.UserOut = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first();
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post does not exist")
    
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == user.id)

    found_vote = vote_query.first()

    if vote.dir == schemas.VoteDir.ADD:
        if not found_vote:
            new_vote = models.Vote(user_id=user.id, post_id=vote.post_id)
            db.add(new_vote)
            db.commit()
        return {'msg': "successfully added vote"}
    else:
        if found_vote:
            vote_query.delete(synchronize_session=False)
            db.commit()
        return {'msg': "successfully deleted vote"}

            

        
        
