from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from .base import get_valid_api_key, get_invalid_api_key


def test_read_main(client: TestClient, db: Session):
    response = client.get("/")
    assert response.status_code == 401
    assert response.json() == {"detail": "Permission denied"}

def test_read_stat(client: TestClient, db: Session):
    headers = get_valid_api_key()
    response = client.post("/newPasswordReseted/", headers=headers)
    assert response.status_code == 200
    assert response.json() == None