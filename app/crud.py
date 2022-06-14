from statistics import mode
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

def delete_user(db: Session, uid : str):
    db.query(models.User).filter(models.User.uid == uid).delete()
    db.commit()

def update_user(db: Session, user:schemas.UserBase, uid: str ):
    db.query(models.User).filter(models.User.uid == uid)\
        .update({**user.dict()})
    db.commit()

def get_users(db: Session, skip : int, limit : int) :
    return db.query(models.User).offset(skip).limit(limit).all()

def count_users(db:Session) :
    return db.query(models.User).count()