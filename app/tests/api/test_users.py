from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.schemas import users as schemas
from .base import get_valid_api_key, get_invalid_api_key


def test_read_main_invalid_token(client: TestClient, db: Session):
    headers = get_invalid_api_key()
    response = client.get("/", headers=headers)
    assert response.status_code == 401


def test_read_main(client: TestClient, db: Session):
    headers = get_valid_api_key()
    response = client.get("/", headers=headers)
    assert response.status_code == 200


def test_get_users(client: TestClient, db: Session):
    headers = get_valid_api_key()
    response = client.get("/users/", headers=headers)
    assert response.status_code == 200
    assert type(response.json()) == list


def test_get_usersWithFilters(client: TestClient, db: Session):
    headers = get_valid_api_key()

    response = client.get("/users/?name_filter=Hola", headers=headers)
    assert response.status_code == 200
    assert type(response.json()) == list

    response = client.get("/users/?email_filter=Jorge", headers=headers)
    assert response.status_code == 200
    assert type(response.json()) == list


def test_get_user_with_db_empty(client: TestClient, db: Session):
    headers = get_valid_api_key()
    response = client.get("/users/ID_INVALIDO", headers=headers)
    assert response.status_code == 404


def test_cant_users(client: TestClient, db: Session):
    headers = get_valid_api_key()
    response = client.get("/users/", headers=headers)
    assert response.status_code == 200


def test_delete_user_invalid_user(client: TestClient, db: Session, mocker):
    headers = get_valid_api_key()
    mocker.patch(
        "app.utils.firebase_logic.delete_user",
        return_value=None)
    response = client.delete("/users/1234", headers=headers)
    assert response.status_code == 200


def test_read_passwordsResets(client: TestClient, db: Session, mocker):
    mocker.patch(
        "app.utils.firebase_logic.get_passwords_resets",
        return_value={"5": 5})
    headers = get_valid_api_key()
    response = client.get("/passwordsResets/", headers=headers)
    assert response.status_code == 200
    assert response.json() == {"5": 5}


def test_read_logins(client: TestClient, db: Session, mocker):
    mocker.patch(
        "app.utils.firebase_logic.get_logins",
        return_value={"1999-25-02": 5})
    headers = get_valid_api_key()
    response = client.get("/Logins/", headers=headers)
    assert response.status_code == 200
    assert response.json() == {"1999-25-02": 5}


def test_read_SinUpStats(client: TestClient, db: Session, mocker):
    mocker.patch(
        "app.utils.firebase_logic.get_singUp_stats",
        return_value={"federated": 8, "manual": 2})
    headers = get_valid_api_key()
    response = client.get("/SingUpStats/", headers=headers)
    assert response.status_code == 200
    assert response.json() == {"federated": 8, "manual": 2}


def test_read_blocked_stats(client: TestClient, db: Session, mocker):
    mocker.patch(
        "app.utils.firebase_logic.get_blocked_stats",
        return_value={"federated": 8, "manual": 2})
    headers = get_valid_api_key()
    response = client.get("/blockedStats/", headers=headers)
    assert response.status_code == 200
    assert response.json() == {"federated": 8, "manual": 2}


def test_new_password_reseted(client: TestClient, db: Session, mocker):
    mocker.patch(
        "app.utils.firebase_logic.notify_password_reseted",
        return_value=None)
    headers = get_valid_api_key()
    response = client.post("/newPasswordReseted/", headers=headers)
    assert response.status_code == 200


def test_new_login(client: TestClient, db: Session, mocker):
    mocker.patch(
        "app.utils.firebase_logic.notify_login_attempt",
        return_value=None)
    headers = get_valid_api_key()
    response = client.post("/newLogin/?uid=12", headers=headers)
    assert response.status_code == 200


def test_manual_register_user(client: TestClient, db: Session, mocker):
    headers = get_valid_api_key()
    mocker.patch(
        "app.utils.firebase_logic.manual_register",
        return_value=schemas.User(
            uid="12345",
            email="hola@hola.com",
            name="Jorge Dinosaurio",
            subscription='Regular',
            disabled=False,
            admin=False,
            federated=False
        ))
    mocker.patch(
        "app.utils.api_wallet.create_wallet",
        return_value=None)
    response = client.post("/manual_register/", headers=headers, json={
        "name": "Jorge Dinosaurio",
        "email": "xd",
        "password": "123",
    })
    assert response.status_code == 200
    assert response.json()["uid"] == "12345"


def test_change_admin_status(client: TestClient, db: Session, mocker):
    headers = get_valid_api_key()
    mocker.patch(
        "app.utils.firebase_logic.manual_register",
        return_value=schemas.User(
            uid="12345",
            email="hola@hola.com",
            name="Jorge Dinosaurio",
            subscription='Regular',
            disabled=False,
            admin=False,
            federated=False
        ))
    mocker.patch(
        "app.utils.api_wallet.create_wallet",
        return_value=None)
    response = client.post("/manual_register/", headers=headers, json={
        "name": "Jorge Dinosaurio",
        "email": "xd",
        "password": "123",
    })
    assert response.status_code == 200
    assert response.json()["uid"] == "12345"

    #  User Created, now testing the change of admin status
    response = client.patch(
        "/user/12345/admin_status/?admin=False",
        headers=headers)
    assert response.status_code == 200
    assert not response.json()["admin"]

    #  User Created, now testing the change of admin status
    response = client.patch(
        "/user/12345/admin_status/?admin=True",
        headers=headers)
    assert response.status_code == 200
    assert response.json()["admin"]


def test_sub_status(client: TestClient, db: Session, mocker):
    headers = get_valid_api_key()
    mocker.patch(
        "app.utils.firebase_logic.manual_register",
        return_value=schemas.User(
            uid="12345",
            email="hola@hola.com",
            name="Jorge Dinosaurio",
            subscription='Regular',
            disabled=False,
            admin=False,
            federated=False
        ))
    mocker.patch(
        "app.utils.api_wallet.create_wallet",
        return_value=None)
    response = client.post("/manual_register/", headers=headers, json={
        "name": "Jorge Dinosaurio",
        "email": "xd",
        "password": "123",
    })
    assert response.status_code == 200
    assert response.json()["uid"] == "12345"

    #  User Created, now testing the change of subs status
    response = client.patch(
        "/user/12345/subscription_status/?subscription=Premium",
        headers=headers)
    assert response.status_code == 200
    assert response.json()["subscription"] == "Premium"

    response = client.patch(
        "/user/12345/subscription_status/?subscription=Jorge",
        headers=headers)
    assert response.status_code == 200
    assert not response.json()["subscription"] == "Premium"


def test_disabled_status(client: TestClient, db: Session, mocker):
    headers = get_valid_api_key()
    mocker.patch(
        "app.utils.firebase_logic.manual_register",
        return_value=schemas.User(
            uid="12345",
            email="hola@hola.com",
            name="Jorge Dinosaurio",
            subscription='Regular',
            disabled=False,
            admin=False,
            federated=False
        ))
    mocker.patch(
        "app.utils.api_wallet.create_wallet",
        return_value=None)
    response = client.post("/manual_register/", headers=headers, json={
        "name": "Jorge Dinosaurio",
        "email": "xd",
        "password": "123",
    })
    assert response.status_code == 200
    assert response.json()["uid"] == "12345"

    mocker.patch(
        "app.utils.firebase_logic.disable",
        return_value=None)
    mocker.patch(
        "app.utils.firebase_logic.enable",
        return_value=None)
    #  User Created, now testing the change of disabled status
    response = client.patch(
        "/disabled_status/12345?disabled=false",
        headers=headers)
    assert response.status_code == 200
    assert not response.json()["disabled"]

    response = client.patch(
        "/disabled_status/12345?disabled=true",
        headers=headers)
    assert response.status_code == 200
    assert response.json()["disabled"]


def test_put_user(client: TestClient, db: Session, mocker):
    headers = get_valid_api_key()
    mocker.patch(
        "app.utils.firebase_logic.get_user",
        return_value=schemas.User(
            uid="1234567",
            email="hola@hola3.com",
            name="Jorge Dinosaurio",
            subscription='Regular',
            disabled=False,
            admin=False,
            federated=False
        ))
    mocker.patch(
        "app.utils.api_wallet.create_wallet",
        return_value=None)
    response = client.put("/users/1234567", headers=headers)

    assert response.status_code == 200
    assert response.json()["uid"] == "1234567"


def test_update_name(client: TestClient, db: Session, mocker):
    headers = get_valid_api_key()
    mocker.patch(
        "app.utils.firebase_logic.manual_register",
        return_value=schemas.User(
            uid="12345",
            email="hola@hola.com",
            name="Jorge Dinosaurio",
            subscription='Regular',
            disabled=False,
            admin=False,
            federated=False
        ))
    mocker.patch(
        "app.utils.api_wallet.create_wallet",
        return_value=None)
    response = client.post("/manual_register/", headers=headers, json={
        "name": "Jorge Dinosaurio",
        "email": "xd",
        "password": "123",
    })
    assert response.status_code == 200
    assert response.json()["uid"] == "12345"
    #  user generated, now testing name.

    response = client.patch(
        "/user/12345/update_name/?name=Carlitox", headers=headers)
    assert response.status_code == 200
    assert response.json()["name"] == "Carlitox"

    response = client.patch(
        "/user/12345/update_name/?name=Carlitox2", headers=headers)
    assert response.status_code == 200
    assert not response.json()["name"] == "Carlitox"

    response = client.patch(
        "/user/12345absurdo22/update_name/?name=Carlitox2", headers=headers)
    assert response.status_code == 404


def test_photo(client: TestClient, db: Session, mocker):
    headers = get_valid_api_key()
    mocker.patch(
        "app.utils.firebase_logic.manual_register",
        return_value=schemas.User(
            uid="12345",
            email="hola@hola.com",
            name="Jorge Dinosaurio",
            subscription='Regular',
            disabled=False,
            admin=False,
            federated=False
        ))
    mocker.patch(
        "app.utils.api_wallet.create_wallet",
        return_value=None)
    response = client.post("/manual_register/", headers=headers, json={
        "name": "Jorge Dinosaurio",
        "email": "xd",
        "password": "123",
    })
    assert response.status_code == 200
    assert response.json()["uid"] == "12345"
    #  user generated, now testing photo.

    response = client.patch(
        "/user/12345/update_photo/?photo=www.google.com", headers=headers)
    assert response.status_code == 200
    assert response.json()["photo_url"] == "www.google.com"

    response = client.patch(
        "/user/12345/update_photo/?photo=www.fb.com", headers=headers)
    assert response.status_code == 200
    assert not response.json()["photo_url"] == "www.google.com"

    response = client.patch(
        "/user/12345absurdo22/update_photo/?photo=www.fb.com", headers=headers)
    assert response.status_code == 404


def test_follow(client: TestClient, db: Session, mocker):
    headers = get_valid_api_key()
    mocker.patch(
        "app.utils.firebase_logic.get_user",
        return_value=schemas.User(
            uid="1234567",
            email="hola@hola3.com",
            name="Jorge Dinosaurio",
            subscription='Regular',
            disabled=False,
            admin=False,
            federated=False
        ))
    mocker.patch(
        "app.utils.api_wallet.create_wallet",
        return_value=None)
    response = client.put("/users/1234567", headers=headers)

    assert response.status_code == 200
    assert response.json()["uid"] == "1234567"

    mocker.patch(
        "app.utils.firebase_logic.get_user",
        return_value=schemas.User(
            uid="12345678",
            email="hola@hola34.com",
            name="El amigo de Jorge Dinosaurio",
            subscription='Regular',
            disabled=False,
            admin=False,
            federated=False
        ))
    response = client.put("/users/12345678", headers=headers)

    response = client.post(
        "users/follow?user_id=1234567&user_id_to_follow=12345678",
        headers=headers)
    assert not response.status_code == 404


def test_follow_and_unfollow(client: TestClient, db: Session, mocker):
    headers = get_valid_api_key()
    mocker.patch(
        "app.utils.firebase_logic.get_user",
        return_value=schemas.User(
            uid="1234567",
            email="hola@hola3.com",
            name="Jorge Dinosaurio",
            subscription='Regular',
            disabled=False,
            admin=False,
            federated=False
        ))
    mocker.patch(
        "app.utils.api_wallet.create_wallet",
        return_value=None)
    response = client.put("/users/1234567", headers=headers)

    assert response.status_code == 200
    assert response.json()["uid"] == "1234567"

    mocker.patch(
        "app.utils.firebase_logic.get_user",
        return_value=schemas.User(
            uid="12345678",
            email="hola@hola34.com",
            name="El amigo de Jorge Dinosaurio",
            subscription='Regular',
            disabled=False,
            admin=False,
            federated=False
        ))
    response = client.put("/users/12345678", headers=headers)

    response = client.post(
        "users/follow?user_id=1234567&user_id_to_follow=12345678",
        headers=headers)
    assert not response.status_code == 404

    response = client.post(
        "users/unfollow?user_id=1234567&user_id_to_unfollow=12345678",
        headers=headers)
    assert response.status_code == 200


def test_follow_itself(client: TestClient, db: Session, mocker):
    headers = get_valid_api_key()
    mocker.patch(
        "app.utils.firebase_logic.get_user",
        return_value=schemas.User(
            uid="1234567",
            email="hola@hola3.com",
            name="Jorge Dinosaurio",
            subscription='Regular',
            disabled=False,
            admin=False,
            federated=False
        ))
    mocker.patch(
        "app.utils.api_wallet.create_wallet",
        return_value=None)
    response = client.put("/users/1234567", headers=headers)

    mocker.patch(
        "app.utils.firebase_logic.get_user",
        return_value=schemas.User(
            uid="12345678",
            email="hola@hola34.com",
            name="El amigo de Jorge Dinosaurio",
            subscription='Regular',
            disabled=False,
            admin=False,
            federated=False
        ))
    response = client.put("/users/12345678", headers=headers)

    response = client.post(
        "users/follow?user_id=1234567&user_id_to_follow=1234567",
        headers=headers)
    assert response.status_code == 400  # you can't follow yourself


def test_add_and_del_genre(client: TestClient, db: Session, mocker):
    headers = get_valid_api_key()
    mocker.patch(
        "app.utils.firebase_logic.get_user",
        return_value=schemas.User(
            uid="1234567",
            email="hola@hola3.com",
            name="Jorge Dinosaurio",
            subscription='Regular',
            disabled=False,
            admin=False,
            federated=False
        ))
    mocker.patch(
        "app.utils.api_wallet.create_wallet",
        return_value=None)
    response = client.put("/users/1234567", headers=headers)

    assert response.status_code == 200
    assert response.json()["uid"] == "1234567"

    response = client.post(
        "users/add_genre?user_id=1234567&genre_id=123",
        headers=headers)
    assert response.status_code == 200

    response = client.post(
        "users/del_genre?user_id=1234567&genre_id=123",
        headers=headers)
    assert response.status_code == 200


def test_decode_token(client: TestClient, db: Session, mocker):
    headers = get_valid_api_key()
    mocker.patch(
        "app.utils.firebase_logic.get_user",
        return_value=schemas.User(
            uid="1234567",
            email="hola@hola3.com",
            name="Jorge Dinosaurio",
            subscription='Regular',
            disabled=False,
            admin=False,
            federated=False
        ))
    mocker.patch(
        "app.utils.api_wallet.create_wallet",
        return_value=None)
    response = client.put("/users/1234567", headers=headers)

    assert response.status_code == 200
    assert response.json()["uid"] == "1234567"

    #  Creamos un usuario de juguete, ahora asumimos que el token es valido.
    mocker.patch(
        "app.utils.firebase_logic.decode_token",
        return_value="1234567")

    response = client.post(
        "/decode_token/?id_token=1234567",
        headers=headers)
    assert response.status_code == 200
