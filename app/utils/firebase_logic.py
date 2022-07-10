from datetime import datetime
import firebase_admin
from firebase_admin import auth
from firebase_admin import credentials
from firebase_admin import db
from sqlalchemy.orm import Session
from app.schemas import users as schemas
from app.cruds import users as crud
import os

cred = credentials.Certificate({
    "type": "service_account",
    "project_id": "spotifiuby-bc6da",
    "private_key_id": os.environ['FB_PRIVATE_KEY_ID'],
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDH9L44YejNTe2m\nN/0ZUrs+U6gk9tsUAJbdR1pnPNfLuVwlycz8UpECSBPjPmC32wveAicZs15y5EmY\n7nWI5LsvkntcLPJk4OyPOdVU+UrNWaZETtbn5eiUAT99Rrnd/OHXQQyb1zLFSgrs\nuVwIF4GoMIHvjzyhWNUkvG1cmXHmxH11ql6xGX5m1OR3uCsW5nMecgRIGVmZIHQB\nVGsYUXh6iaTo2tHWa7p6vzkCgvmoLG37DQ1ruHVJ/qlV1l9txvxuEFtnLLZwdPc3\nc36cZWc8WU3F+nGsTdiWwb85JT6o9VZQxfT+E5wKFHUfOa9o6Yj5DPHafqMyvPjb\nCV8pGBOnAgMBAAECggEAGdM0pN2TDr5rh4CgXMlAS7rMSFyQS6i5KMJ9ckCmcmEc\nqKNuqSwUycxQspSCM1zEJJv3PCzcHE9QaMMWRQ7y/3WWHyqNnT/Q7b1UyJEbUHhY\nBBHWqcQaN3tjHXqpU3rExGNaDd/2ZmAQwdA9iwIA30hx5Q8v5SWEVHv4TUcNh0tL\nXxxtl9sSLnJ1gClfv0w3LmCPnBQxI8DIjNi4vzefVQ6/980nJ+ERx66aQi/MqMDj\n3luaJ2doWONJ/RD7NAn9jG8OeWBMSdh3vkx0lymFOYNXUb6EiQWQwhdeWSzcJ5wa\nmieoN2mPl2KaA+xeyMNAVM22qT6dwhUhOFPs7ZHYyQKBgQD480aO1yK5mQMp3Bp9\nmeXE7HiB2yZ7tu6Jgg0Z3vQhnpKIrBdqwTiO7JLgRYoaPs2QZKYJ5yc3zRXqnMSw\nbBNrrHJlTlIbooH/dH8ItExSDlM2WjIDOpB0BTolDlKKyhlDn2W0/9bmXCVKAmSX\nB06b7AZb5EODjIhZ5sPVDjbzLQKBgQDNnkqgjOk1P2X/2WEM2WahZNf9I32csCR/\nmAfTeqlY74VcGOEnjuWseap6cnKkVlxBfORaE9vxEjeljwzbQ47hllGbT1yLozX4\n0SyG+eN1H+R+rvYFjMkVf9pbsiGCjDGHE4BrQDUOxX0qIQErn3RH2nxYEpofJ36M\ns+/jpOb2owKBgDUtSgITBFDe1WUopeP0brcsx+T9GfBNOBDZXdEL5dwUkjptgCcG\nlP06nXkYgZJvndtdFHaDEMaDoU3XJNCGlXNnh5wKKdHLWbdmfAgw8yiH9NBkXdCA\nvwB5aV0m/Qy2dMUUFFagW5gjULfJYRE9t1XpCcaxMJa1+x4xA93LxoMVAoGAZnjN\nrkerbXsEBUa7ZCDwUdyk+6X1UuJBvkjxFYba4NS1vJk1lHZVpegYet+QnK/hWE26\nq92bzf+LNfodqSR5D5nPX7xkXb7gBfmQ3E+q+NMFF9FwEIICMLHAC9SxeJMPl8az\nSD/+cTcg0p8SK0BTPf/32hijMIWJPuvp0KR86ksCgYBMklcMpHmhqcfEFnNkrHX0\nMyIH/PeA4k4+e717BWNARESwzJWYrOz4W40FiJUmDNdQcz0md9DyeGQNw9XWcOKi\nrYbyezeHdc3pwcngljIDfg54zQ08MD3qxpaneE7MlCeVLjQkI5PdOx6pRfxaGdPm\nJvpVubFPpomdYNGtOeQ/LA==\n-----END PRIVATE KEY-----\n", # noqa
    "client_email": os.environ['FB_CLIENT_EMAIL'],
    "client_id": os.environ['FB_CLIENT_ID'],
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs", # noqa
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-3povb%40spotifiuby-bc6da.iam.gserviceaccount.com" # noqa
})

firebase_admin.initialize_app(
    cred,
    {"databaseURL": "https://spotifiuby-bc6da-default-rtdb.firebaseio.com/"}
)


def get_user(uid):
    user_fb = auth.get_user(uid)
    return schemas.User(
        uid=uid,
        email=user_fb.email,
        name=user_fb.display_name,
        subscription='None',
        disabled=bool(user_fb.disabled),
        admin=False,
        # Si el log fue manual esto deberia ser falso.
        federated=user_fb.email_verified
    )


async def delete_user(uid):
    auth.delete_user(uid)


def sync_users(db: Session):
    auth.list_users()
    for user in auth.list_users().iterate_all():
        crud.create_user(db=db, user=schemas.User(
            uid=user.uid,
            email=user.email,
            name=user.display_name,
            subscription='Regular',
            disabled=bool(user.disabled),
            admin=False,
            federated=bool(user.email_verified),
            # Si el log fue manual esto deberia ser falso.
            photo_url=user.photo_url,
        ))


def manual_register(user: schemas.UserToRegister):
    user_fb = auth.create_user(
        email=user.email,
        email_verified=False,
        password=user.password,
        disabled=False,
        display_name=user.name)
    return schemas.User(
        uid=user_fb.uid,
        email=user_fb.email,
        name=user_fb.display_name,
        subscription='Regular',
        disabled=bool(user_fb.disabled),
        admin=False,
        federated=False  # Si el log fue manual esto deberia ser falso.
    )


def disable(uid: str):
    auth.update_user(uid, disabled=True)


def enable(uid: str):
    auth.update_user(uid, disabled=False)


def decode_token(id_token: str):
    decoded_token = auth.verify_id_token(id_token)
    uid = decoded_token['uid']
    return uid


def notify_password_reseted():
    date = datetime.today().strftime('%Y-%m-%d')
    ref = db.reference('/passwordRecoveries/' + date)
    ref.transaction(lambda x: x + 1 if x is not None else 1)


def notify_login_attempt(uid: str):
    user_fb = auth.get_user(uid)
    date = datetime.today().strftime('%Y-%m-%d')
    if (bool(user_fb.email_verified)):
        ref = db.reference('/loginAttempts/federated/' + date)
        ref.transaction(lambda x: x + 1 if x is not None else 1)
    else:
        ref = db.reference('/loginAttempts/manual/' + date)
        ref.transaction(lambda x: x + 1 if x is not None else 1)


def get_logins():
    ref = db.reference('/loginAttempts')
    return ref.get()


def get_passwords_resets():
    ref = db.reference('/passwordRecoveries')
    return ref.get()


def get_singUp_stats():
    password = 0
    federated = 0
    auth.list_users()
    for user in auth.list_users().iterate_all():
        if(user.email_verified):
            federated += 1
        else:
            password += 1
    return {'email_password': password, 'federated': federated}


def get_blocked_stats():
    blocked = 0
    enabled = 0
    auth.list_users()
    for user in auth.list_users().iterate_all():
        if(user.disabled):
            blocked += 1
        else:
            enabled += 1
    return {'enabled': enabled, 'blocked': blocked}


def update_noti_token(user_id: str, token: str):
    db.reference('/NotiTokens/' + user_id).set(token)
    return token


def get_noti_token(user_id: str):
    return db.reference('/NotiTokens/' + user_id).get()
