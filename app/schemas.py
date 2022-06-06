from typing import Union
from pydantic import BaseModel

class UserBase(BaseModel):
    email : str
    name : str
    subscription : str

    
class User(UserBase):
    uid : str # Firebase user id
    federated : bool
    admin : bool
    disabled : bool
    class Config:
        orm_mode = True