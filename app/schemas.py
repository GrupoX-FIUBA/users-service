from typing import Union
from pydantic import BaseModel
from sqlalchemy import union

class UserBase(BaseModel):
    name : Union[str, None] = None
    subscription : str
    federated : bool
    admin : bool
    disabled : bool
    
class User(UserBase):
    uid : str # Firebase user id
    email : str
    class Config:
        orm_mode = True 