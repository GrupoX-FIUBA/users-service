#!/bin/sh

alembic upgrade head

datadog-agent run > /dev/null &
/opt/datadog-agent/embedded/bin/trace-agent --config=/etc/datadog-agent/datadog.yaml > /dev/null &
/opt/datadog-agent/embedded/bin/process-agent --config=/etc/datadog-agent/datadog.yaml > /dev/null &

DD_SERVICE="users-service" \
DD_ENV="prod" \
DD_LOGS_INJECTION=true \
ddtrace-run uvicorn app.main:app --host 0.0.0.0 --port $PORT
