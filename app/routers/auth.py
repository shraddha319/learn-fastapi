from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import database, schemas, models, utils, oauth2
from sqlalchemy.orm import Session

router = APIRouter(tags=['Authentication'], prefix='/auth')

@router.post('/login', response_model=schemas.Token)
def login(credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user does not exist")
    
    # verify pwd with hashed pwd from db
    if not utils.verify_password(credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid credentials")
    
    # generate & return access token
    access_token = oauth2.create_access_token({'user_id': user.id})

    return {'access_token': access_token, 'token_type': 'bearer'}
    