from sqlalchemy.orm import Session
from . import models, schemas

#Users 
def get_user(db : Session, uid : str):
    return db.query(models.User).filter(models.User.uid == uid).first()

def create_user(db: Session, user : schemas.User):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

#Subs
def get_subscriptions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Subscription).offset(skip).limit(limit).all()

def create_subscription(db: Session, sub : schemas.SubscriptionBase):
    db_sub = models.Subscription(description = sub.description)
    db.add(db_sub)
    db.commit()
    db.refresh(db_sub)
    return db_sub

def delete_subscription(db: Session, id : int):
    db.query(models.Subscription).filter(models.Subscription.id == id).delete()
    db.commit()