from statistics import mode
from pyparsing import FollowedBy
from sqlalchemy.orm import Session
from . import models, schemas
from sqlalchemy import insert

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

def change_admin(db :Session, uid: str, admin : bool):
    db.query(models.User).filter(models.User.uid == uid)\
        .update({models.User.admin : admin})
    db.commit()

def change_subscription(db :Session, uid: str, sub : str):
    db.query(models.User).filter(models.User.uid == uid)\
        .update({models.User.subscription : sub})
    db.commit()

def change_name(db :Session, uid: str, name : str):
    db.query(models.User).filter(models.User.uid == uid)\
        .update({models.User.name : name})
    db.commit()

def change_disable_status(db :Session, uid: str, disabled : bool):
    db.query(models.User).filter(models.User.uid == uid)\
        .update({models.User.disabled : disabled})
    db.commit()

def follow (db: Session, user_id : str, user_id_to_follow : str ) :
    user_db = db.query(models.User).filter(models.User.uid == user_id).first()
    user_db.following.append(user_id_to_follow)
    db.commit()
    return db.query(models.User).filter(models.User.uid == user_id).first()
    '''db.query(models.User).filter(models.User.uid == user_id)\
        .update({models.User.following : user_id_to_follow})
    db.commit()'''