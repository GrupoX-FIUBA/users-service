from fastapi import APIRouter

from app.endpoints import users
from app.endpoints.base import response_codes


router = APIRouter()
router.include_router(users.router, responses={401: response_codes[401]})
