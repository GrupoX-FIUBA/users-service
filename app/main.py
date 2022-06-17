import string
import xdrlib
from pydantic import BaseModel
from fastapi  import FastAPI, HTTPException, Depends
from typing import List
from sqlalchemy import false
from sqlalchemy.orm import Session
from . import crud, models, schemas

import app.firebase_logic as fl

from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

#models.Base.metadata.drop_all(engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()


@app.get("/")
def read_root():
	return {"msg": "Servicio de Usuarios"}

@app.get("/users/{user_id}")
def get_user(user_id : str, db: Session = Depends(get_db)):
	try:
		user : schemas.User = crud.get_user(db = db, uid = user_id)
	except BaseException as e:
		raise HTTPException(status_code=404, detail='error: {0}'.format(e))
	return user

@app.get("/users/")
def get_users(skip : int = 0 , limit : int  = 100, db : Session = Depends(get_db)):
	try:
		return crud.get_users(db = db, skip = skip, limit = limit)
	except BaseException as e:
		raise HTTPException(status_code=400, detail='error: {0}'.format(e))

#Usuario ya se debe encontrar cargado en FireBase
@app.put("/users/{user_id}")
def put_user(user_id: str, db: Session = Depends(get_db)):
	try:
		user = fl.get_user(user_id)
		user = crud.get_user(db = db, uid= user_id)
		if ( user == None ) :
			user = crud.create_user(db = db, user = user)
	except BaseException as e:
		raise HTTPException(status_code=400, detail='error: {0}'.format(e))
	return user

@app.get("/count_users/")
def count_users( db : Session = Depends(get_db) ):
	try:
		return crud.count_users(db = db)
	except BaseException as e:
		raise HTTPException(status_code=400, detail='error: {0}'.format(e))

@app.post("/syncFB/")
def sync_with_firebase( db : Session = Depends(get_db) ):
	try:
		fl.sync_users(db = db)
	except BaseException as e:
		raise HTTPException(status_code=400, detail='error: {0}'.format(e))

@app.delete("/users/{user_id}")
def delete_user(user_id : str, db: Session = Depends(get_db)):
	try:
		fl.delete_user(uid = user_id)
		user = crud.delete_user(db = db, uid = user_id)
	except BaseException as e:
		raise HTTPException(status_code=400, detail='error: {0}'.format(e))
	return user

@app.patch("/user/admin_status/{user_id}")
def change_admin(user_id : str, admin:bool, db: Session = Depends(get_db)):
	try:
		user = crud.change_admin(db = db, uid = user_id, admin = admin)
	except BaseException as e:
		raise HTTPException(status_code=400, detail='error: {0}'.format(e))
	return user

@app.patch("/user/subscription_status/{user_id}")
def change_sub(user_id : str, subscription:str, db: Session = Depends(get_db)):
	try:
		user = crud.change_subscription(db = db, uid = user_id, sub = subscription)
	except BaseException as e:
		raise HTTPException(status_code=400, detail='error: {0}'.format(e))
	return user

@app.patch("/user/update_name/{user_id}")
def change_name(user_id : str, name:str, db: Session = Depends(get_db)):
	try:
		user = crud.change_name(db = db, uid = user_id, name = name)
	except BaseException as e:
		raise HTTPException(status_code=400, detail='error: {0}'.format(e))
	return user

#Recibe email y password de un usuario a dar de alta.
@app.post("/manual_register/")
def manual_register(user : schemas.UserToRegister, db: Session = Depends(get_db)):
	try:
		fb_user = fl.manual_register(user)
		return crud.create_user(db = db, user = fb_user)
	except BaseException as e:
		raise HTTPException(status_code=400, detail='error: {0}'.format(e))

@app.patch("/disable/{user_id}")
def disable_user(user_id, db: Session = Depends(get_db)):
	try:
		fl.disable(user_id)
		crud.change_enable_status(db = db, uid= user_id,disabled = True)
	except BaseException as e:
		raise HTTPException(status_code=400, detail='error: {0}'.format(e))

@app.patch("/enable/{user_id}")
def enable_user(user_id : str, db: Session = Depends(get_db)):
	try:
		fl.enable(user_id)
		crud.change_enable_status(db = db, uid= user_id,disabled = False)
	except BaseException as e:
		raise HTTPException(status_code=400, detail='error: {0}'.format(e))


@app.post("/users/follow")
def follow_user(user_id : str, user_id_to_follow : str, db: Session = Depends(get_db)):
	try:
		return crud.follow(db = db, user_id= user_id, user_id_to_follow=user_id_to_follow)
	except BaseException as e:
		raise HTTPException(status_code=400, detail='error: {0}'.format(e))

@app.post("/users/unfollow")
def unfollow_user(user_id : str, user_id_to_unfollow : str, db: Session = Depends(get_db)):
	try:
		return crud.unfollow(db = db, user_id= user_id, user_id_to_unfollow=user_id_to_unfollow)
	except BaseException as e:
		raise HTTPException(status_code=400, detail='error: {0}'.format(e))


# Devuelve el id del usuario en base a su token.
# En caso de que no se encuentre el usuario se devuelve código 400.
@app.post("/decode_token/")
async def decode_token(id_token:str):
	try:
		return fl.decode_token(id_token)
	except BaseException as e : 
		raise HTTPException(status_code=400, detail="Token no valido")

@app.get("/users/{user_id}/followers/")
def get_followers(user_id : str, db: Session = Depends(get_db)):
	try:
		user = crud.get_user(db = db, uid = user_id)
	except BaseException as e:
		raise HTTPException(status_code=400, detail='error: {0}'.format(e))
	return user.following