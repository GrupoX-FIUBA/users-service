from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from .database import Base

class User(Base):
    __tablename__ = 'users'

    uid = Column(String, primary_key=True, index=True)
    email = Column(String, unique=False, index=True)
    name = Column(String, unique=False, index=True)
    disabled = Column(Boolean, default=False)
    federated = Column(Boolean, default=False)
    admin = Column(Boolean, default=False)
    subscription = Column(String, unique=False, default = "Regular")