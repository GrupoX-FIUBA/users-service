from fastapi import FastAPI, Depends

from app.endpoints.base import get_api_key
from app.routes.api import router as api_router

tags_metadata = [
    {
        "name": "Getters",
        "description":
        "Operaciones generales, tanto para ADMIN como para usuarios regulares",
    },
    {
        "name": "Administrador",
        "description": "Operaciones para cambiar estado de usuario",
    },
    {
        "name": "Interacciones de Usuario",
        "description": "Operaciones que puede hacer el usuario a su perfil",
    },
    {
        "name": "Validación de Usuario",
        "description": "Verificar quien es quien",
    },
    {
        "name": "Estadisticas",
        "description": "Operadores para generar y obtener estadisticas",
    },
    {
        "name": "Notificaciones",
        "description": "Operaciones para notificaciones",
    }
]

app = FastAPI(dependencies=[Depends(get_api_key)],
              openapi_tags=tags_metadata)

app.include_router(api_router)
