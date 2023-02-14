from pydantic import BaseModel, EmailStr
from datetime import datetime
from enum import Enum

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: str
    email: str
    created_at: datetime

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    id: str

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: str
    created_at: datetime
    owner: UserOut
    
    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True

class VoteDir(str, Enum):
    ADD = 1
    DEL = 0

    class Config:
        use_enum_values = True


class Vote(BaseModel):
    post_id: int
    dir: VoteDir


