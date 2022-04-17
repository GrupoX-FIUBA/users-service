# Template repository for FastAPI microservices

This is a template to use as a starting point for FastAPI microservice repositories. Once configured, it will run the tests on every pull request to `main`, and will automatically deploy to corresponding Heroku app when a push to `main` occurs.

## To Do after fork/create-from-template

Simply go to the repository settings, _Actions secrets_ and create a new _repository secret_ with name `HEROKU_APP_NAME` and the name of the Heroku app in the _value_ field.

In the `app` directory there's a very simple example of a FastAPI app with tests.

## Local development

To run the application there are two options:

### With Docker

Run `docker-compose up` to start the app in port 8000 or `PORT=xxxx docker-compose up` to use a specific `xxxx` port.

### With _virtualenv_

- First of all create a _virtualenv_ (_i.e._ `python3 -m venv venv`) and activate it (`source venv/bin/activate`).
- Upgrade pip and install the dependencies: `pip install --upgrade pip && pip install -r requirements`.
- Run the app with:
	```bash
	uvicorn app.main:app --host 0.0.0.0 --port 8000
	```

## Tests

Again, there are two options. Note that the _virtualenv_ option is naturally faster.

### With Docker

Run the command:

```bash
docker-compose run --rm fastapi sh -c "pip install -q -q -r /code/requirements.dev.txt && sh /code/test.sh"
```

### With _virtualenv_

- Be sure to be in the virtual environment, if not, activate it (_i.e._ `source venv/bin/activate`).
- The first time, install the dev dependencies: `pip install -r requirements.dev.txt`.
- Run the linter and tests with `./test.sh`.

## Docs

The documentation is generated automatically by FastAPI. It's available in the server at `/docs` (Swagger) and `/redoc` (ReDoc)