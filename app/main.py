import xdrlib
from fastapi  import FastAPI
from pydantic import BaseModel
from fastapi  import FastAPI, HTTPException
import os

import firebase_admin
from   firebase_admin import auth
from   firebase_admin import credentials

cred = credentials.Certificate({
  "type": "service_account",
  "project_id": "spotifiuby-bc6da",
  "private_key_id": os.environ['FB_PRIVATE_KEY_ID'],
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDH9L44YejNTe2m\nN/0ZUrs+U6gk9tsUAJbdR1pnPNfLuVwlycz8UpECSBPjPmC32wveAicZs15y5EmY\n7nWI5LsvkntcLPJk4OyPOdVU+UrNWaZETtbn5eiUAT99Rrnd/OHXQQyb1zLFSgrs\nuVwIF4GoMIHvjzyhWNUkvG1cmXHmxH11ql6xGX5m1OR3uCsW5nMecgRIGVmZIHQB\nVGsYUXh6iaTo2tHWa7p6vzkCgvmoLG37DQ1ruHVJ/qlV1l9txvxuEFtnLLZwdPc3\nc36cZWc8WU3F+nGsTdiWwb85JT6o9VZQxfT+E5wKFHUfOa9o6Yj5DPHafqMyvPjb\nCV8pGBOnAgMBAAECggEAGdM0pN2TDr5rh4CgXMlAS7rMSFyQS6i5KMJ9ckCmcmEc\nqKNuqSwUycxQspSCM1zEJJv3PCzcHE9QaMMWRQ7y/3WWHyqNnT/Q7b1UyJEbUHhY\nBBHWqcQaN3tjHXqpU3rExGNaDd/2ZmAQwdA9iwIA30hx5Q8v5SWEVHv4TUcNh0tL\nXxxtl9sSLnJ1gClfv0w3LmCPnBQxI8DIjNi4vzefVQ6/980nJ+ERx66aQi/MqMDj\n3luaJ2doWONJ/RD7NAn9jG8OeWBMSdh3vkx0lymFOYNXUb6EiQWQwhdeWSzcJ5wa\nmieoN2mPl2KaA+xeyMNAVM22qT6dwhUhOFPs7ZHYyQKBgQD480aO1yK5mQMp3Bp9\nmeXE7HiB2yZ7tu6Jgg0Z3vQhnpKIrBdqwTiO7JLgRYoaPs2QZKYJ5yc3zRXqnMSw\nbBNrrHJlTlIbooH/dH8ItExSDlM2WjIDOpB0BTolDlKKyhlDn2W0/9bmXCVKAmSX\nB06b7AZb5EODjIhZ5sPVDjbzLQKBgQDNnkqgjOk1P2X/2WEM2WahZNf9I32csCR/\nmAfTeqlY74VcGOEnjuWseap6cnKkVlxBfORaE9vxEjeljwzbQ47hllGbT1yLozX4\n0SyG+eN1H+R+rvYFjMkVf9pbsiGCjDGHE4BrQDUOxX0qIQErn3RH2nxYEpofJ36M\ns+/jpOb2owKBgDUtSgITBFDe1WUopeP0brcsx+T9GfBNOBDZXdEL5dwUkjptgCcG\nlP06nXkYgZJvndtdFHaDEMaDoU3XJNCGlXNnh5wKKdHLWbdmfAgw8yiH9NBkXdCA\nvwB5aV0m/Qy2dMUUFFagW5gjULfJYRE9t1XpCcaxMJa1+x4xA93LxoMVAoGAZnjN\nrkerbXsEBUa7ZCDwUdyk+6X1UuJBvkjxFYba4NS1vJk1lHZVpegYet+QnK/hWE26\nq92bzf+LNfodqSR5D5nPX7xkXb7gBfmQ3E+q+NMFF9FwEIICMLHAC9SxeJMPl8az\nSD/+cTcg0p8SK0BTPf/32hijMIWJPuvp0KR86ksCgYBMklcMpHmhqcfEFnNkrHX0\nMyIH/PeA4k4+e717BWNARESwzJWYrOz4W40FiJUmDNdQcz0md9DyeGQNw9XWcOKi\nrYbyezeHdc3pwcngljIDfg54zQ08MD3qxpaneE7MlCeVLjQkI5PdOx6pRfxaGdPm\nJvpVubFPpomdYNGtOeQ/LA==\n-----END PRIVATE KEY-----\n",
  "client_email": os.environ['FB_CLIENT_EMAIL'],
  "client_id": os.environ['FB_CLIENT_ID'],
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-3povb%40spotifiuby-bc6da.iam.gserviceaccount.com"
})
firebase_admin.initialize_app(cred)

app = FastAPI()

@app.get("/")
def read_root():
	return {"msg": "Servicio de Usuarios"}


# Devuelve una lista de todos los usuarios
# Este metodo es provisorio, hasta que se implemente el paginado.
@app.get("/users/")
async def get_users():
	users_dic = {}
	n = 0
	page = auth.list_users()
	for user in auth.list_users().iterate_all():
		users_dic[n] = {'id':user.uid, 'mail' : user.email}
		n+=1

	return users_dic



class user_to_register(BaseModel):
    email: str
    password: str
#Recibe email y password de un usuario a dar de alta.
@app.post("/register/")
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

@app.post("/register/")
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
	except firebase_admin._auth_utils.EmailAlreadyExistsError:
		raise HTTPException(status_code=400, detail="No se pudo eliminar el usuario")

	return {'detail' : 'Usuario Corractemente eliminado'}