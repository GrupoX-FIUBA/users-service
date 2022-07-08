from fastapi import Security, HTTPException, status
from fastapi.security.api_key import APIKeyHeader

from app.db.session import SessionLocal
from app.core.settings import API_KEY_NAME, API_KEY


api_key_header = APIKeyHeader(name = API_KEY_NAME, auto_error = False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_api_key(
    api_key_header: str = Security(api_key_header),
):
    if api_key_header == API_KEY:
        return api_key_header

    raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
                        detail = "Permission denied")


response_codes = {
    401: {
        "description": "Unauthorized",
        "content": {
            "application/json": {
                "example": {"detail": "string"}
            }
        }
    },
    404: {
        "description": "Not Found",
        "content": {
            "application/json": {
                "example": {"detail": "string"}
            }
        }
    },
}
