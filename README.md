[![codecov](https://codecov.io/gh/GrupoX-FIUBA/users-service/branch/main/graph/badge.svg?token=VXS3E2BKR7)](https://codecov.io/gh/GrupoX-FIUBA/users-service)

# User Microservice

This microservice manages the users related topics.

## Local development

- First, create a `.env` file to reduce commands length, setting up the COMPOSE_PROFILES variable to "dev" (`echo COMPOSE_PROFILES=dev >> .env`). Also, put there the necessary `FB_` env variables.
- It's also recommended to build the container after a pull: `docker-compose build`.
- Then you can run the app: `docker-compose up`. It will also run a postgres container for development.

The app will start at port 8000 as default. You can use a specific port by setting the PORT env variable either at the `.env` file or within each command.

### Changes to database models

To create database migrations for changes done in _models_ files, run `docker-compose exec development alembic revision --autogenerate -m "Title of migration"`.

To apply changes to existing-running container, you can either restart it (`docker-compose restart`) or run the migrations (`docker-compose exec development alembic upgrade head`).

## Tests

To run the tests, simply execute `docker-compose --profile test up`. You can add `--exit-code-from test` to pass the exit code of the test script to the shell session.

Again, it's recommended to build the container after a pull. In this case, you must build with the _test_ profile: `docker-compose --profile test build`.

## Docs

The documentation is generated automatically by FastAPI. It's available in the server at `/docs` (Swagger) and `/redoc` (ReDoc)
