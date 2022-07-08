FROM python:3.9-slim as base

WORKDIR /code

COPY ./requirements.txt ./requirements.txt
COPY ./alembic.ini ./alembic.ini
COPY ./alembic ./alembic

RUN pip install --upgrade pip
RUN pip install -r ./requirements.txt


# Test stage
FROM base as test

COPY ./requirements.dev.txt ./requirements.dev.txt
COPY ./test.sh ./test.sh

RUN pip install -r ./requirements.dev.txt

CMD sh test.sh


# Dev stage
FROM base as development

COPY ./start.sh ./start.sh

CMD sh start.sh


# Prod stage
FROM base as production

# Install Heroku GPG dependencies
RUN apt-get update \
 && apt-get install -y gnupg apt-transport-https gpg-agent curl ca-certificates

# Copy Datadog configuration
COPY heroku/datadog-config/ /etc/datadog-agent/

COPY heroku/start.sh /code/start.sh

# Add Datadog repository and signing keys
ENV DATADOG_APT_KEYRING="/usr/share/keyrings/datadog-archive-keyring.gpg"
ENV DATADOG_APT_KEYS_URL="https://keys.datadoghq.com"
RUN sh -c "echo 'deb [signed-by=${DATADOG_APT_KEYRING}] https://apt.datadoghq.com/ stable 7' > /etc/apt/sources.list.d/datadog.list"
RUN touch ${DATADOG_APT_KEYRING}
RUN curl -o /tmp/DATADOG_APT_KEY_CURRENT.public "${DATADOG_APT_KEYS_URL}/DATADOG_APT_KEY_CURRENT.public" && \
    gpg --ignore-time-conflict --no-default-keyring --keyring ${DATADOG_APT_KEYRING} --import /tmp/DATADOG_APT_KEY_CURRENT.public
RUN curl -o /tmp/DATADOG_APT_KEY_F14F620E.public "${DATADOG_APT_KEYS_URL}/DATADOG_APT_KEY_F14F620E.public" && \
    gpg --ignore-time-conflict --no-default-keyring --keyring ${DATADOG_APT_KEYRING} --import /tmp/DATADOG_APT_KEY_F14F620E.public
RUN curl -o /tmp/DATADOG_APT_KEY_382E94DE.public "${DATADOG_APT_KEYS_URL}/DATADOG_APT_KEY_382E94DE.public" && \
    gpg --ignore-time-conflict --no-default-keyring --keyring ${DATADOG_APT_KEYRING} --import /tmp/DATADOG_APT_KEY_382E94DE.public

# Install the Datadog agent
RUN apt-get update && apt-get -y --force-yes install --reinstall datadog-agent

# Expose DogStatsD and trace-agent ports
EXPOSE 8125/udp 8126/tcp

COPY ./app ./app

# Use app entrypoint
CMD ["bash", "start.sh"]
