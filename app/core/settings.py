import os

DATABASE_URL = os.environ["DATABASE_URL"].replace("postgres://",
                                                  "postgresql://", 1)

API_KEY_NAME = "X-API-Key"
API_KEY = os.environ.get("X_API_KEY", "prueba")
