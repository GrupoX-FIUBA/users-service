from email import feedparser
import email
from statistics import mode
from tkinter import N
from typing import List
from pyparsing import FollowedBy
from sqlalchemy.orm import Session

from app.firebase_logic import disable
from . import models, schemas
from sqlalchemy import insert
import json

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

    if db_user.genres == None:
        schema_user.genres=[]
    else:
        schema_user.genres=json.loads(db_user.genres)

    return schema_user


def get_user(db : Session, uid : str):
    db_user = db.query(models.User).filter(models.User.uid == uid).first()
    if (db_user == None):
        raise Exception("User not found")
    return dbUser_to_schemaUser(db_user)

def get_users(db: Session, skip : int, limit : int) :
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user : schemas.User):
    db_user = db.query(models.User).filter(models.User.uid == user.uid).first()
    if( db_user == None ): #Si el usuario no esta cargado lo creo.
        db_user = models.User(uid=user.uid,
                            email=user.email,
                            name = user.name,
                            disabled = user.disabled,
                            federated = user.federated,
                            admin = user.admin,
                            subscription = user.subscription,
                            photo_url=user.photo_url,
                        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    return dbUser_to_schemaUser(db_user)

def delete_user(db: Session, uid : str):
    db.query(models.User).filter(models.User.uid == uid).delete()
    db.commit()

def count_users(db:Session) :
    return db.query(models.User).count()

def change_admin(db :Session, uid: str, admin : bool):
    db_user = get_user(db=db, uid = uid)
    db_user.admin = admin
    db.commit()
    return dbUser_to_schemaUser(db_user)

def change_subscription(db :Session, uid: str, sub : str):
    db_user = get_user(db=db, uid = uid)
    db_user.subscription = sub
    db.commit()
    return dbUser_to_schemaUser(db_user)

def change_name(db :Session, uid: str, name : str):
    db_user = get_user(db=db, uid = uid)
    db_user.name = name
    db.commit()
    return dbUser_to_schemaUser(db_user)

def change_photo(db : Session, uid : str, photo : str):
    db_user = get_user(db=db, uid = uid)
    db_user.photo_url = photo
    db.commit()
    return dbUser_to_schemaUser(db_user)

def change_disable_status(db :Session, uid: str, disabled : bool):
    db_user = get_user(db=db, uid = uid)
    db_user.disabled = disabled
    db.commit()
    return dbUser_to_schemaUser(db_user)

def follow (db: Session, user_id : str, user_id_to_follow : str ):
    if (user_id == user_id_to_follow):
        raise Exception("Un usuario no se puede seguir asi mismo")
    user_db = db.query(models.User).filter(models.User.uid == user_id).first()
    user_to_follow = db.query(models.User).filter(models.User.uid == user_id_to_follow).first()
    if (user_db == None or user_to_follow == None):
        raise Exception("User not Found")
    if user_to_follow in user_db.following:
        raise Exception("Usuario A ya sigue a Usuario B")
    user_db.following.append(user_to_follow)
    db.commit()
    return dbUser_to_schemaUser(user_db)

def unfollow (db: Session, user_id : str, user_id_to_unfollow : str ):
    user_db = db.query(models.User).filter(models.User.uid == user_id).first()
    user_to_unfollow = db.query(models.User).filter(models.User.uid == user_id_to_unfollow).first()
    if (user_db == None or user_to_unfollow == None):
        raise Exception("User not Found")
    if user_to_unfollow not in user_db.following:
        raise Exception("Usuario A no sigue a Usuario B")
    user_db.following.remove(user_to_unfollow)
    db.commit()
    return dbUser_to_schemaUser(user_db)

def add_genre(db: Session, user_id : str, genre_id : int ):
    user_db = db.query(models.User).filter(models.User.uid == user_id).first()
    if user_db.genres == None :
        genres = []
    else:
        genres = json.loads(user_db.genres)

    if genre_id not in genres :
        genres.append(genre_id)
    user_db.genres = json.dumps(genres)
    db.commit()
    return dbUser_to_schemaUser(user_db)

def del_genre(db: Session, user_id : str, genre_id : int ):
    user_db = db.query(models.User).filter(models.User.uid == user_id).first()
    if user_db.genres == None :
        genres = []
    else:
        genres = json.loads(user_db.genres)
        
    if genre_id in genres:
        genres.remove(genre_id)
    user_db.genres = json.dumps(genres)
    db.commit()
    return dbUser_to_schemaUser(user_db)

'''
def update_user(db: Session, user:schemas.UserBase, uid: str ):
    db.query(models.User).filter(models.User.uid == uid)\
        .update({**user.dict()})
    db.commit()
'''