from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.cruds import users as crud
from app.models import users as models
from app.schemas import users as schemas
from .base import get_db

from app.utils.api_wallet import create_wallet
from typing import Union
import app.utils.firebase_logic as fl


router = APIRouter(
    #prefix = "",
)


@router.get("/")
def read_root():
    return {"msg": "Servicio de Usuarios"}


@router.get("/users/{user_id}", tags=["Getters"])
def get_user(user_id: str, db: Session = Depends(get_db)):
    try:
        user: schemas.User = crud.get_user(db=db, uid=user_id)
    except BaseException as e:
        raise HTTPException(status_code=404, detail='error: {0}'.format(e))
    return user


@router.get("/users/", tags=["Getters"])
def get_users(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    name_filter: Union[str, None] = None,
    email_filter: Union[str, None] = None
):
    try:
        return crud.get_users(db=db, skip=skip,
                              limit=limit,
                              name_filter=name_filter,
                              email_filter=email_filter)
    except BaseException as e:
        raise HTTPException(status_code=400, detail='error: {0}'.format(e))


@router.get("/cant_users/", tags=["Getters"])
def count_users(db: Session = Depends(get_db)):
    try:
        return crud.count_users(db=db)
    except BaseException as e:
        raise HTTPException(status_code=400, detail='error: {0}'.format(e))

# Usuario ya se debe encontrar cargado en FireBase


@router.put("/users/{user_id}", tags=["Interacciones de Usuario"])
def put_user(user_id: str, db: Session = Depends(get_db)):
    try:
        fb_user = fl.get_user(user_id)
        create_wallet(fb_user.uid)
        user = crud.create_user(db=db, user=fb_user)
    except BaseException as e:
        raise HTTPException(status_code=400, detail='error: {0}'.format(e))
    return user

# Recibe email y password de un usuario a dar de alta, si no existe en FB
# lo registra alli.


@router.post("/manual_register/", tags=["Administrador"])
def manual_register(
        user: schemas.UserToRegister,
        db: Session = Depends(get_db)):
    try:
        fb_user = fl.manual_register(user)
        create_wallet(fb_user.uid)
        return crud.create_user(db=db, user=fb_user)
    except BaseException as e:
        raise HTTPException(status_code=400, detail='error: {0}'.format(e))


@router.delete("/users/{user_id}",
               tags=["Interacciones de Usuario", "Administrador"])
def delete_user(user_id: str, db: Session = Depends(get_db)):
    try:
        fl.delete_user(uid=user_id)
        crud.delete_user(db=db, uid=user_id)
    except BaseException as e:
        raise HTTPException(status_code=400, detail='error: {0}'.format(e))


@router.patch("/user/{user_id}/admin_status/", tags=["Administrador"])
def change_admin(user_id: str, admin: bool, db: Session = Depends(get_db)):
    try:
        user = crud.change_admin(db=db, uid=user_id, admin=admin)
    except BaseException as e:
        raise HTTPException(status_code=404, detail='error: {0}'.format(e))
    return user


@router.patch("/user/{user_id}/subscription_status/", tags=["Administrador"])
def change_subscription(
        user_id: str,
        subscription: str,
        db: Session = Depends(get_db)):
    try:
        user = crud.change_subscription(db=db, uid=user_id, sub=subscription)
    except BaseException as e:
        raise HTTPException(status_code=404, detail='error: {0}'.format(e))
    return user


@router.patch("/user/{user_id}/update_name/",
              tags=["Interacciones de Usuario"])
def change_name(user_id: str, name: str, db: Session = Depends(get_db)):
    try:
        user = crud.change_name(db=db, uid=user_id, name=name)
    except BaseException as e:
        raise HTTPException(status_code=404, detail='error: {0}'.format(e))
    return user


@router.patch("/user/{user_id}/update_photo/",
              tags=["Interacciones de Usuario"])
def change_photo(user_id: str, photo: str, db: Session = Depends(get_db)):
    try:
        user = crud.change_photo(db=db, uid=user_id, photo=photo)
    except BaseException as e:
        raise HTTPException(status_code=404, detail='error: {0}'.format(e))
    return user


@router.patch("/disabled_status/{user_id}", tags=["Administrador"])
def change_disabled_user(
        user_id: str,
        disabled: bool,
        db: Session = Depends(get_db)):
    try:
        if (disabled):
            fl.disable(user_id)
        else:
            fl.enable(user_id)
        return crud.change_disable_status(
            db=db, uid=user_id, disabled=disabled)
    except BaseException as e:
        raise HTTPException(status_code=404, detail='error: {0}'.format(e))


@router.post("/users/follow", tags=["Interacciones de Usuario"])
def follow_user(
        user_id: str,
        user_id_to_follow: str,
        db: Session = Depends(get_db)):
    try:
        return crud.follow(
            db=db,
            user_id=user_id,
            user_id_to_follow=user_id_to_follow)
    except BaseException as e:
        raise HTTPException(status_code=400, detail='error: {0}'.format(e))


@router.post("/users/unfollow", tags=["Interacciones de Usuario"])
def unfollow_user(
        user_id: str,
        user_id_to_unfollow: str,
        db: Session = Depends(get_db)):
    try:
        return crud.unfollow(
            db=db,
            user_id=user_id,
            user_id_to_unfollow=user_id_to_unfollow)
    except BaseException as e:
        raise HTTPException(status_code=400, detail='error: {0}'.format(e))


@router.post("/users/add_genre", tags=["Interacciones de Usuario"])
def add_genre(user_id: str, genre_id: int, db: Session = Depends(get_db)):
    try:
        return crud.add_genre(db=db, user_id=user_id, genre_id=genre_id)
    except BaseException as e:
        raise HTTPException(status_code=400, detail='error: {0}'.format(e))


@router.post("/users/del_genre", tags=["Interacciones de Usuario"])
def del_genre(user_id: str, genre_id: int, db: Session = Depends(get_db)):
    try:
        return crud.del_genre(db=db, user_id=user_id, genre_id=genre_id)
    except BaseException as e:
        raise HTTPException(status_code=400, detail='error: {0}'.format(e))

# Devuelve el id del usuario en base a su token.
# En caso de que no se encuentre el usuario se devuelve código 400.


@router.post("/decode_token/", tags=["Validación de Usuario"])
def decode_token(id_token: str, db: Session = Depends(get_db)):
    try:
        return crud.get_user(db=db, uid=fl.decode_token(id_token))
    except BaseException as e:
        raise HTTPException(status_code=400, detail="Token no valido")

# Notify that the user has requested to change the password.


@router.post("/newPasswordReseted/", tags=["Estadisticas"])
def passwordReseted():
    try:
        fl.get_passwords_resets()
    except BaseException as e:
        raise HTTPException(status_code=400, detail='error: {0}'.format(e))

# Notify that a new login has happened.


@router.post("/newLogin/", tags=["Estadisticas"])
def notify_login(uid: str):
    try:
        fl.notify_login_attempt(uid)
    except BaseException as e:
        raise HTTPException(status_code=400, detail='error: {0}'.format(e))

# Logins stats


@router.get("/Logins/", tags=["Estadisticas"])
def get_logins():
    try:
        return fl.get_logins()
    except BaseException as e:
        raise HTTPException(status_code=400, detail='error: {0}'.format(e))

# Devuelve restauraciones de contraseña


@router.get("/passwordsResets/", tags=["Estadisticas"])
def get_passwords_resets():
    try:
        return fl.get_passwords_resets()
    except BaseException as e:
        raise HTTPException(status_code=400, detail='error: {0}'.format(e))

# Sing up Stats


@router.get("/SingUpStats/", tags=["Estadisticas"])
def singUpStats():
    try:
        return fl.get_singUp_stats()
    except BaseException as e:
        raise HTTPException(status_code=400, detail='error: {0}'.format(e))

# BlockedStats


@router.get("/blockedStats/", tags=["Estadisticas"])
def blockedStats():
    try:
        return fl.get_blocked_stats()
    except BaseException as e:
        raise HTTPException(status_code=400, detail='error: {0}'.format(e))
