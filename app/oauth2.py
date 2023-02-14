from fastapi import Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError, ExpiredSignatureError
from datetime import datetime, timedelta
from . import schemas, database, models
from .config import settings

# key for hashing
SECRET_KEY = settings.jwt_secret_key

# hashing algorithm
ALGORITHM = settings.jwt_algorithm

ACCESS_TOKEN_EXPIRE_MINUTES = settings.jwt_token_expire_minutes

# to be called as a dependency
# will look in the request for that Authorization header, checks if the value is Bearer + some token & returns token as string
# If it doesn't see an Authorization header, or the value doesn't have a Bearer token, it will respond with a 401 status code error (UNAUTHORIZED) directly.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/login')

def create_access_token(payload: dict):
    to_encode = payload.copy()
    expire_at = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode['exp'] = expire_at

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    # verifies signature & expiry
    # returns the payload if valid token
    try: 
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get('user_id')
        
        if not id:
            raise credentials_exception
        
        token_payload = schemas.TokenPayload(id=id)
        return token_payload
    except (JWTError, ExpiredSignatureError):
        raise credentials_exception
    
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid token", headers={'WWW-Authenticate': 'Bearer'})

    token_payload = verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.id == token_payload.id).first()

    return user
    




