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

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

tags_metadata = [
    {
        "name": "Getters",
        "description": "Operaciones generales, tanto para ADMIN como para usuarios regulares",
    },
    {
        "name": "Administrador",
        "description": "Operaciones para cambiar estado de usuario",
    },
	{
        "name": "Interacciones de Usuario",
        "description": "Operaciones que puede hacer el usuario a su perfil desde el cliente",
    },
	{
		"name": "Validación de Usuario",
        "description": "Operaciones que puede hacer el usuario a su perfil desde el cliente",
	}
]

app = FastAPI(openapi_tags=tags_metadata)

@app.get("/")
def read_root():
	return {"msg": "Servicio de Usuarios"}

@app.get("/users/{user_id}",tags=["Getters"])
def get_user(user_id : str, db: Session = Depends(get_db)):
	try:
		user : schemas.User = crud.get_user(db = db, uid = user_id)
	except BaseException as e:
		raise HTTPException(status_code=404, detail='error: {0}'.format(e))
	return user

@app.get("/users/", tags=["Getters"])
def get_users(skip : int = 0 , limit : int  = 100, db : Session = Depends(get_db)):
	try:
		return crud.get_users(db = db, skip = skip, limit = limit)
	except BaseException as e:
		raise HTTPException(status_code=400, detail='error: {0}'.format(e))


@app.get("/cant_users/", tags=["Getters"])
def count_users( db : Session = Depends(get_db) ):
	try:
		return crud.count_users(db = db)
	except BaseException as e:
		raise HTTPException(status_code=400, detail='error: {0}'.format(e))


#Usuario ya se debe encontrar cargado en FireBase
@app.put("/users/{user_id}", tags=["Interacciones de Usuario"])
def put_user(user_id: str, db: Session = Depends(get_db)):
	try:
		fb_user = fl.get_user(user_id)
		user = crud.create_user(db = db, user = fb_user)
	except BaseException as e:
		raise HTTPException(status_code=400, detail='error: {0}'.format(e))
	return user

#Recibe email y password de un usuario a dar de alta, si no existe en FB lo registra alli.
@app.post("/manual_register/", tags=["Administrador"])
def manual_register(user : schemas.UserToRegister, db: Session = Depends(get_db)):
	try:
		fb_user = fl.manual_register(user)
		return crud.create_user(db = db, user = fb_user)
	except BaseException as e:
		raise HTTPException(status_code=400, detail='error: {0}'.format(e))


@app.delete("/users/{user_id}", tags=["Interacciones de Usuario", "Administrador"])
def delete_user(user_id : str, db: Session = Depends(get_db)):
	try:
		fl.delete_user(uid = user_id)
		crud.delete_user(db = db, uid = user_id)
	except BaseException as e:
		raise HTTPException(status_code=400, detail='error: {0}'.format(e))

@app.patch("/user/{user_id}/admin_status/", tags=["Administrador"])
def change_admin(user_id : str, admin:bool, db: Session = Depends(get_db)):
	try:
		user = crud.change_admin(db = db, uid = user_id, admin = admin)
	except BaseException as e:
		raise HTTPException(status_code=404, detail='error: {0}'.format(e))
	return user

@app.patch("/user/{user_id}/subscription_status/", tags=["Administrador"])
def change_subscription(user_id : str, subscription:str, db: Session = Depends(get_db)):
	try:
		user = crud.change_subscription(db = db, uid = user_id, sub = subscription)
	except BaseException as e:
		raise HTTPException(status_code=404, detail='error: {0}'.format(e))
	return user

@app.patch("/user/{user_id}/update_name/", tags=["Interacciones de Usuario"])
def change_name(user_id : str, name:str, db: Session = Depends(get_db)):
	try:
		user = crud.change_name(db = db, uid = user_id, name = name)
	except BaseException as e:
		raise HTTPException(status_code=404, detail='error: {0}'.format(e))
	return user

@app.patch("/user/{user_id}/update_photo/", tags=["Interacciones de Usuario"])
def change_photo(user_id : str, photo:str, db: Session = Depends(get_db)):
	try:
		user = crud.change_photo(db = db, uid = user_id, photo = photo)
	except BaseException as e:
		raise HTTPException(status_code=404, detail='error: {0}'.format(e))
	return user

@app.patch("/disabled_status/{user_id}", tags=["Administrador"])
def change_disabled_user(user_id : str, disabled : bool, db: Session = Depends(get_db)):
	try:
		if (disabled == True):
			fl.disable(user_id)
		else:	
			fl.enable(user_id)
		return crud.change_disable_status(db = db, uid= user_id,disabled = disabled)
	except BaseException as e:
		raise HTTPException(status_code=404, detail='error: {0}'.format(e))

@app.post("/users/follow", tags=["Interacciones de Usuario"])
def follow_user(user_id : str, user_id_to_follow : str, db: Session = Depends(get_db)):
	try:
		return crud.follow(db = db, user_id= user_id, user_id_to_follow=user_id_to_follow)
	except BaseException as e:
		raise HTTPException(status_code=400, detail='error: {0}'.format(e))

@app.post("/users/unfollow", tags=["Interacciones de Usuario"])
def unfollow_user(user_id : str, user_id_to_unfollow : str, db: Session = Depends(get_db)):
	try:
		return crud.unfollow(db = db, user_id= user_id, user_id_to_unfollow=user_id_to_unfollow)
	except BaseException as e:
		raise HTTPException(status_code=400, detail='error: {0}'.format(e))

@app.post("/users/add_genre", tags=["Interacciones de Usuario"])
def add_genre(user_id : str, genre_id : int , db: Session = Depends(get_db)):
	try:
		return crud.add_genre(db = db, user_id=user_id, genre_id = genre_id)
	except BaseException as e:
		raise HTTPException(status_code=400, detail='error: {0}'.format(e))

@app.post("/users/del_genre", tags=["Interacciones de Usuario"])
def del_genre(user_id : str, genre_id : int, db: Session = Depends(get_db)):
	try:
		return crud.del_genre(db = db, user_id=user_id, genre_id = genre_id)
	except BaseException as e:
		raise HTTPException(status_code=400, detail='error: {0}'.format(e))

# Devuelve el id del usuario en base a su token.
# En caso de que no se encuentre el usuario se devuelve código 400.
@app.post("/decode_token/", tags=["Validación de Usuario"])
def decode_token(id_token:str, db: Session = Depends(get_db)):
	try:
		return crud.get_user (db=db, uid=fl.decode_token(id_token))
	except BaseException as e : 
		raise HTTPException(status_code=400, detail="Token no valido")
'''
@app.post("/syncFB/")
def sync_with_firebase( db : Session = Depends(get_db) ):
	try:
		fl.sync_users(db = db)
	except BaseException as e:
		raise HTTPException(status_code=400, detail='error: {0}'.format(e))
'''