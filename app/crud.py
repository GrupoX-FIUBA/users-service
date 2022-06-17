from email import feedparser
from statistics import mode
from pyparsing import FollowedBy
from sqlalchemy.orm import Session
from . import models, schemas
from sqlalchemy import insert

def dbUser_to_schemaUser (db_user):
    schema_user = schemas.User(
        uid = db_user.uid,
        email = db_user.email,
        name = db_user.name,
        disabled = db_user.disabled,
        federated = db_user.federated,
        admin = db_user.admin,
        subscription = db_user.subscription,
        photo_url=db_user.photo_url,    
    )
    for x in db_user.following :
        schema_user.following.append(schemas.UserReduced(
            uid =x.uid,
            name=x.name,
            email=x.email,
            photo_url=x.photo_url,
        ))
    for x in db_user.followers :
        schema_user.followers.append(schemas.UserReduced(
            uid =x.uid,
            name=x.name,
            email=x.email,
            photo_url=x.photo_url,
        ))
    return db_user

def get_user(db : Session, uid : str):
    db_user = db.query(models.User).filter(models.User.uid == uid).first()
    if (db_user == None):
        raise Exception("User not found")
    return dbUser_to_schemaUser(db_user)

def get_users(db: Session, skip : int, limit : int) :
    return db.query(models.User).offset(skip).limit(limit).all()


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

def follow (db: Session, user_id : str, user_id_to_follow : str ):
    if (user_id == user_id_to_follow):
        raise Exception("Un usuario no se puede seguir asi mismo")
    user_db = db.query(models.User).filter(models.User.uid == user_id).first()
    user_to_follow = db.query(models.User).filter(models.User.uid == user_id_to_follow).first()
    if user_to_follow in user_db.following:
        raise Exception("Usuario A ya sigue a Usuario B")
    user_db.following.append(user_to_follow)
    db.commit()

def unfollow (db: Session, user_id : str, user_id_to_unfollow : str ):
    user_db = db.query(models.User).filter(models.User.uid == user_id).first()
    user_id_to_unfollow = db.query(models.User).filter(models.User.uid == user_id_to_unfollow).first()
    if user_id_to_unfollow not in user_db.following:
        raise Exception("Usuario A no sigue a Usuario B")
    user_db.following.remove(user_id_to_unfollow)
    db.commit()

def get_followers(db: Session, user_id : str):
    return db.query(models.User).filter(models.User.uid == user_id).first()