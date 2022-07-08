#!/bin/sh

alembic upgrade head

args=""
if [ $DEBUG ] && [ $DEBUG != "0" ]; then
	args="--reload"
fi

# echo $args
uvicorn app.main:app --host 0.0.0.0 --port $PORT $args
