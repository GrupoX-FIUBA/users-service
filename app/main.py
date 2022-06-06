import string
import xdrlib
from pydantic import BaseModel
from fastapi  import FastAPI, HTTPException, Depends
from typing import List
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
def get_user(user_id, db: Session = Depends(get_db)):
	try:
		user = crud.get_user(db = db, uid = user_id)
	except BaseException as e:
		raise HTTPException(status_code=400, detail='error: {0}'.format(e))
	return user

@app.put("/users/{user_id}")
def put_user(user_id, db: Session = Depends(get_db)):
	try:
		user = fl.get_user(user_id)
		user = crud.get_user(db = db, uid= user_id)
		print(user)
		if ( user == None ) :
			user = crud.create_user(db = db, user = user)
	except BaseException as e:
		raise HTTPException(status_code=400, detail='error: {0}'.format(e))
	return user

'''
@app.get("/users/")
async def get_users(skip : int = 0 , limit : int  = 100):
	if ( (skip < 0) or (limit < 0) ):
		raise HTTPException(status_code=400, detail="El offset y el limite tienen que ser positivos")

	users_page = []
	n = 0
	page = auth.list_users()
	for user in auth.list_users().iterate_all():
		if ( n == (skip+limit) ):
			break

		if( n >= skip ) :
			users_page.append ( {'index': n,
								 'id'   : user.uid,
								 'mail' : user.email,
								 'name' : user.display_name,
								 'disabled': user.disabled ,
								 'admin' : False,
								 'subscription' : 'Regular',
								 'federated' : False
								 }
							   )
		n+=1

	return users_page

class user_to_register(BaseModel):
    email:    str
    password: str

#Recibe email y password de un usuario a dar de alta.
@app.post("/manual_register/")
async def create_user(_user : user_to_register ):
	try:
		user = auth.create_user(
			email= _user.email,
			email_verified= False,
			password= _user.password,
			disabled= False)
	except firebase_admin._auth_utils.EmailAlreadyExistsError:
		raise HTTPException(status_code=400, detail="Email ya Registrado")

	return  {'detail' : "Usuario Correctamente generado",
	        'user_id' : user.uid ,
			'email' : user.email }

@app.delete("/{user_id}")
async def delete_user(user_id):

	try:
		auth.delete_user(user_id)
	except firebase_admin._auth_utils.UserNotFoundError:
		raise HTTPException(status_code=400, detail="El usuario no existe")
	return {'detail' : 'Usuario Corractemente eliminado'}


@app.patch("/disable/{user_id}")
async def disable_user(user_id):
	try:
		auth.update_user(user_id, disabled = True)
	except firebase_admin._auth_utils.UserNotFoundError:
		raise HTTPException(status_code=400, detail="El usuario no existe")
	return {'detail' : 'Usuario Corractemente deshabilitado'}

@app.patch("/enable/{user_id}")
async def enable_user(user_id):
	try:
		auth.update_user(user_id, disabled = False)
	except firebase_admin._auth_utils.UserNotFoundError:
		raise HTTPException(status_code=400, detail="El usuario no existe")
	return {'detail' : 'Usuario Corractemente habilitado'}

#Devuelve la cantidad de usuarios registrados.
@app.get("/registered_users/")
async def registered_users():
	n = 0
	page = auth.list_users()
	for user in auth.list_users().iterate_all():
		n+=1
	return {'usuarios_registrados': n}

# Devuelve el usuario en base a su token.
# En caso de que no se encuentre el usuario se devuelve codigo 400.
@app.post("/decode_token/")
async def decode_token(id_token):
	try: 
		decoded_token = auth.verify_id_token(id_token)
		uid = decoded_token['uid']
		user = auth.get_user(uid)
	except firebase_admin._auth_utils.InvalidIdTokenError : 
		raise HTTPException(status_code=400, detail="Token no valido")
	return {	'index': 0,
				'id'   : user.uid,
				'mail' : user.email,
				'name' : user.display_name,
				'photo' : user.photoURL,
				'disabled': user.disabled,
				'admin' : False,
				'subscription' : 'Regular',
				'federated' : False
			}

@app.post("/User/", response_model=schemas.User)
def insert_user(user_id: string, db: Session = Depends(get_db)):
	#try:
	#	user : schemas.User = firebase.get_user(user_id)
	#except BaseException as e:
	#	raise HTTPException(status_code=400, detail='error: {0}'.format(e))
    #return crud.create_user(db=db, user=user)

## Subscriptions CRUD.
@app.post("/subscriptions/", response_model=schemas.Subscription)
def create_subscription(sub: schemas.SubscriptionBase, db: Session = Depends(get_db)):
    return crud.create_subscription(db=db, sub=sub)

@app.get("/subscriptions/", response_model = List[schemas.Subscription] )
def read_subscriptions (skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_subscriptions (db=db, skip = skip , limit = 100)

@app.delete("/subscriptions/", response_model = List[schemas.Subscription] )
def del_subscriptions (id: int ,db: Session = Depends(get_db) ):
    crud.delete_subscription (db = db, id = id)
'''