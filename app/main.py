import string
import xdrlib

import requests
from pydantic import BaseModel
from fastapi  import FastAPI, HTTPException, Depends, Security, Request

from fastapi.security.api_key import  APIKeyHeader, APIKey

from app.api_wallet import create_wallet
from typing import List, Union
from starlette.status import HTTP_403_FORBIDDEN
from sqlalchemy.orm import Session
from . import crud, models, schemas
import app.firebase_logic as fl
from .database import SessionLocal, engine
import os

#Seguridad
API_KEY = os.environ.get("API_KEY")
API_KEY_NAME = "access_token"

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)
async def get_api_key(
    api_key_header: str = Security(api_key_header),
):
    if api_key_header == API_KEY:
        return api_key_header
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )

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
	},
	{
		"name": "Estadisticas",
		"description": "Operadores para generar y obtener estadisticas",
	},
]

app = FastAPI(openapi_tags=tags_metadata)

@app.get("/")
def read_root():
	return {"msg": "Servicio de Usuarios"}

@app.get("/users/{user_id}",tags=["Getters"])
def get_user(user_id : str, db: Session = Depends(get_db), api_key: APIKey = Depends(get_api_key)):
	try:
		user : schemas.User = crud.get_user(db = db, uid = user_id)
	except BaseException as e:
		raise HTTPException(status_code=404, detail='error: {0}'.format(e))
	return user

@app.get("/users/", tags=["Getters"])
def get_users(
				db : Session = Depends(get_db),
				skip : int = 0,
				limit : int  = 100,
				name_filter : Union[str, None] = None,
				email_filter : Union[str, None] = None,
				api_key: APIKey = Depends(get_api_key)
				):
	try:
		return crud.get_users(db = db, skip = skip,
					 			limit = limit,
							 	name_filter = name_filter,
								email_filter = email_filter)
	except BaseException as e:
		raise HTTPException(status_code=400, detail='error: {0}'.format(e))


@app.get("/cant_users/", tags=["Getters"])
def count_users( db : Session = Depends(get_db), api_key: APIKey = Depends(get_api_key) ):
	try:
		return crud.count_users(db = db)
	except BaseException as e:
		raise HTTPException(status_code=400, detail='error: {0}'.format(e))

#Usuario ya se debe encontrar cargado en FireBase
@app.put("/users/{user_id}", tags=["Interacciones de Usuario"])
def put_user(user_id: str, db: Session = Depends(get_db), api_key: APIKey = Depends(get_api_key)):
	try:
		fb_user = fl.get_user(user_id)
		create_wallet(fb_user.uid)
		user = crud.create_user(db = db, user = fb_user)
	except BaseException as e:
		raise HTTPException(status_code=400, detail='error: {0}'.format(e))
	return user

#Recibe email y password de un usuario a dar de alta, si no existe en FB lo registra alli.
@app.post("/manual_register/", tags=["Administrador"])
def manual_register(user : schemas.UserToRegister, db: Session = Depends(get_db), api_key: APIKey = Depends(get_api_key)):
	try:
		fb_user = fl.manual_register(user)
		create_wallet(fb_user.uid)
		return crud.create_user(db = db, user = fb_user)
	except BaseException as e:
		raise HTTPException(status_code=400, detail='error: {0}'.format(e))

@app.delete("/users/{user_id}", tags=["Interacciones de Usuario", "Administrador"])
def delete_user(user_id : str, db: Session = Depends(get_db), api_key: APIKey = Depends(get_api_key)):
	try:
		fl.delete_user(uid = user_id)
		crud.delete_user(db = db, uid = user_id)
	except BaseException as e:
		raise HTTPException(status_code=400, detail='error: {0}'.format(e))

@app.patch("/user/{user_id}/admin_status/", tags=["Administrador"])
def change_admin(user_id : str, admin:bool, db: Session = Depends(get_db), api_key: APIKey = Depends(get_api_key)):
	try:
		user = crud.change_admin(db = db, uid = user_id, admin = admin)
	except BaseException as e:
		raise HTTPException(status_code=404, detail='error: {0}'.format(e))
	return user

@app.patch("/user/{user_id}/subscription_status/", tags=["Administrador"])
def change_subscription(user_id : str, subscription:str, db: Session = Depends(get_db), api_key: APIKey = Depends(get_api_key)):
	try:
		user = crud.change_subscription(db = db, uid = user_id, sub = subscription)
	except BaseException as e:
		raise HTTPException(status_code=404, detail='error: {0}'.format(e))
	return user

@app.patch("/user/{user_id}/update_name/", tags=["Interacciones de Usuario"])
def change_name(user_id : str, name:str, db: Session = Depends(get_db), api_key: APIKey = Depends(get_api_key)):
	try:
		user = crud.change_name(db = db, uid = user_id, name = name)
	except BaseException as e:
		raise HTTPException(status_code=404, detail='error: {0}'.format(e))
	return user

@app.patch("/user/{user_id}/update_photo/", tags=["Interacciones de Usuario"])
def change_photo(user_id : str, photo:str, db: Session = Depends(get_db), api_key: APIKey = Depends(get_api_key)):
	try:
		user = crud.change_photo(db = db, uid = user_id, photo = photo)
	except BaseException as e:
		raise HTTPException(status_code=404, detail='error: {0}'.format(e))
	return user

@app.patch("/disabled_status/{user_id}", tags=["Administrador"])
def change_disabled_user(user_id : str, disabled : bool, db: Session = Depends(get_db), api_key: APIKey = Depends(get_api_key)):
	try:
		if (disabled == True):
			fl.disable(user_id)
		else:	
			fl.enable(user_id)
		return crud.change_disable_status(db = db, uid= user_id,disabled = disabled)
	except BaseException as e:
		raise HTTPException(status_code=404, detail='error: {0}'.format(e))

@app.post("/users/follow", tags=["Interacciones de Usuario"])
def follow_user(user_id : str, user_id_to_follow : str, db: Session = Depends(get_db), api_key: APIKey = Depends(get_api_key)):
	try:
		return crud.follow(db = db, user_id= user_id, user_id_to_follow=user_id_to_follow)
	except BaseException as e:
		raise HTTPException(status_code=400, detail='error: {0}'.format(e))

@app.post("/users/unfollow", tags=["Interacciones de Usuario"])
def unfollow_user(user_id : str, user_id_to_unfollow : str, db: Session = Depends(get_db), api_key: APIKey = Depends(get_api_key)):
	try:
		return crud.unfollow(db = db, user_id= user_id, user_id_to_unfollow=user_id_to_unfollow)
	except BaseException as e:
		raise HTTPException(status_code=400, detail='error: {0}'.format(e))

@app.post("/users/add_genre", tags=["Interacciones de Usuario"])
def add_genre(user_id : str, genre_id : int , db: Session = Depends(get_db), api_key: APIKey = Depends(get_api_key)):
	try:
		return crud.add_genre(db = db, user_id=user_id, genre_id = genre_id)
	except BaseException as e:
		raise HTTPException(status_code=400, detail='error: {0}'.format(e))

@app.post("/users/del_genre", tags=["Interacciones de Usuario"])
def del_genre(user_id : str, genre_id : int, db: Session = Depends(get_db), api_key: APIKey = Depends(get_api_key)):
	try:
		return crud.del_genre(db = db, user_id=user_id, genre_id = genre_id)
	except BaseException as e:
		raise HTTPException(status_code=400, detail='error: {0}'.format(e))

# Devuelve el id del usuario en base a su token.
# En caso de que no se encuentre el usuario se devuelve código 400.
@app.post("/decode_token/", tags=["Validación de Usuario"])
def decode_token(id_token:str, db: Session = Depends(get_db), api_key: APIKey = Depends(get_api_key)):
	try:
		return crud.get_user (db=db, uid=fl.decode_token(id_token))
	except BaseException as e : 
		raise HTTPException(status_code=400, detail="Token no valido")

## Notify that the user has requested to change the password.
@app.post("/newPasswordReseted/",tags=["Estadisticas"])
def passwordReseted(api_key: APIKey = Depends(get_api_key)):
	try:
		fl.get_passwords_resets()
	except BaseException as e:
		raise HTTPException(status_code=400, detail='error: {0}'.format(e))

## Notify that a new login has happened.
@app.post("/newLogin/",tags=["Estadisticas"])
def notify_login(uid : str, api_key: APIKey = Depends(get_api_key)):
	try:
		fl.notify_login_attempt( uid )
	except BaseException as e:
		raise HTTPException(status_code=400, detail='error: {0}'.format(e))

## Logins stats 
@app.get("/Logins/",tags=["Estadisticas"])
def get_logins(api_key: APIKey = Depends(get_api_key)):
	try:
		return fl.get_logins()
	except BaseException as e:
		raise HTTPException( status_code=400, detail='error: {0}'.format(e) )

## Devuelve restauraciones de contraseña
@app.get("/passwordsResets/",tags=["Estadisticas"])
def get_passwords_resets(api_key: APIKey = Depends(get_api_key)):
	try:
		return fl.get_passwords_resets()
	except BaseException as e:
		raise HTTPException( status_code=400, detail='error: {0}'.format(e) )

## Sing up Stats
@app.get("/SingUpStats/",tags=["Estadisticas"])
def singUpStats(api_key: APIKey = Depends(get_api_key)):
	try:
		return fl.get_singUp_stats()
	except BaseException as e:
		raise HTTPException( status_code=400, detail='error: {0}'.format(e) )

## BlockedStats
@app.get("/blockedStats/",tags=["Estadisticas"])
def blockedStats(api_key: APIKey = Depends(get_api_key)):
	try:
		return fl.get_blocked_stats()
	except BaseException as e:
		raise HTTPException( status_code=400, detail='error: {0}'.format(e) )
