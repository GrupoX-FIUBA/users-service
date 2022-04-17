FROM python:3.9-alpine

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
COPY ./requirements.dev.txt /code/requirements.dev.txt
COPY ./test.sh /code/test.sh

RUN pip install --upgrade pip
RUN pip install -r /code/requirements.txt

COPY ./app /code/app

# ENV PORT=8000
# EXPOSE $PORT

CMD uvicorn app.main:app --host 0.0.0.0 --port $PORT
