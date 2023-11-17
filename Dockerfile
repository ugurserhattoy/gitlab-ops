FROM python:3.9-alpine

# RUN apk add --no-cache ca-certificates && update-ca-certificates
RUN apk update && apk upgrade --no-cache
RUN apk add --no-cache \
    curl \
    unzip \
    vim

COPY ./api/requirements.txt /tmp/

RUN python -m pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --upgrade -r /tmp/requirements.txt
#api files
RUN mkdir /opt/gitlab-ops-api
COPY ./api /opt/gitlab-ops-api

WORKDIR /opt/gitlab-ops-api

ENTRYPOINT [ "python", "main.py" ]
