from typing import Union, List
from pydantic import BaseModel

class UserReduced(BaseModel):
    uid : str # Firebase user id
    email: str
    name: Union[str, None] = None
    photo_url : Union[str, None] = None

class UserToRegister(BaseModel):
    name: Union[str, None] = None
    email: str
    password: str

class UserBase(BaseModel):
    name : Union[str, None] = None
    subscription : str
    federated : bool
    admin : bool
    disabled : bool
    photo_url : Union[str, None] = None
    following: List[UserReduced] = []
    followers: List[UserReduced] = []
    genres: List[int] = []

class User(UserBase):
    uid : str # Firebase user id
    email : str
    class Config:
        orm_mode = True 
