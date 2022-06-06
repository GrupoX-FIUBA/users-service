from typing import Union
from pydantic import BaseModel

class SubscriptionBase(BaseModel):
    description: str

class Subscription(SubscriptionBase):
    id: int
    class Config:
        orm_mode = True

    
class User(BaseModel):
    uid : str
    email : str
    name : str
    federated : bool
    admin : bool
    subscription_id : int
    class Config:
        orm_mode = True