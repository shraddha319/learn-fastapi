from fastapi import status, HTTPException, Depends, Response, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas, oauth2
from sqlalchemy import desc, func

router = APIRouter(prefix='/posts', tags=['Posts'])

@router.get("/", response_model=list[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), user: schemas.UserOut = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: str = ""):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()

    posts = db.query(models.Post, func.count(models.Vote.user_id).label('votes')).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).offset(skip).limit(limit).all()

    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), user: schemas.UserOut = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    new_post = models.Post(owner_id=user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@router.get("/latest", response_model=schemas.PostOut)
def get_post(db: Session = Depends(get_db), user: schemas.UserOut = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts ORDER BY created_at DESC LIMIT 1""")
    # latest_post = cursor.fetchone()

    latest_post = db.query(models.Post, func.count(models.Vote.user_id).label('votes')).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).order_by(desc(models.Post.created_at)).limit(1).first()

    return latest_post

@router.get("/{post_id}", response_model=schemas.PostOut)
def get_post(post_id: int, db: Session = Depends(get_db), user: schemas.UserOut = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(post_id),))
    # post = cursor.fetchone()

    post = db.query(models.Post, func.count(models.Vote.user_id).label('votes')).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).filter(models.Post.id == post_id).group_by(models.Post.id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {post_id} not found")
    
    return post

@router.put("/{post_id}", response_model=schemas.Post)
def update_post(post_id: int, update_post: schemas.PostCreate, db: Session = Depends(get_db), user: schemas.UserOut = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title=%s, content=%s, published=%s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(post_id)))

    # updated_post = cursor.fetchone()
    # conn.commit();

    post_query = db.query(models.Post).filter(models.Post.id == post_id)

    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {post_id} not found")
    
    if post.owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"not allowed")
    
    post_query.update(update_post.dict(), synchronize_session=False)
    db.commit()
    
    return post_query.first()


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db), user: schemas.UserOut = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(post_id),))

    # deleted_post = cursor.fetchone()
    # conn.commit();

    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {post_id} not found")
    
    if post.owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"not allowed")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)