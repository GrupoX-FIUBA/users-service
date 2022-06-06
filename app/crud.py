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

def update_user(db: Session, User:schemas.User ):
    db.query(models.User).filter(models.User.uid == User.uid)\
        .update(**User.dict())