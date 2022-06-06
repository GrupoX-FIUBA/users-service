from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base

class User(Base):
    __tablename__ = "user"

    uid = Column(String, primary_key=True, index=True)
    email = Column(String, unique=False, index=True)
    name = Column(String, unique=False, index=True)
    federated = Column(Boolean, default=False)
    admin = Column(Boolean, default=False)
    subscription_id = Column(Integer, ForeignKey("subscription.id"))
    subscription = relationship("Subscription")

class Subscription (Base):
    __tablename__ = "subscription"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True, unique=True)
    #No quiero la relación bidireccional
    #users = relationship("User", back_populates = "subscription") 