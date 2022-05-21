from typing import Union
from pydantic import BaseModel


class Subscription(BaseModel):
    id: int
    title: str
    description: Union[str, None] = None

class User(BaseModel):
    uid : str
    email : str
    name : str
    federated : bool
    admin : bool
    subscription : int