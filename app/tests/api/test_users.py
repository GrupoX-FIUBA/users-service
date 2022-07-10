from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

#  from app import schemas

from .base import get_valid_api_key   # , get_invalid_api_key


def test_read_main_invalid_token(client: TestClient, db: Session):
    response = client.get("/")
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
