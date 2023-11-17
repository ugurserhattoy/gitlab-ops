FROM python:3.9-alpine

# RUN apk add --no-cache ca-certificates && update-ca-certificates
RUN apk update && apk upgrade --no-cache
RUN apk add --no-cache \
    curl \
    unzip \
    vim
    
COPY ./requirements.txt /tmp/

RUN python -m pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --upgrade -r /tmp/requirements.txt
#cli files
RUN mkdir /opt/gitlab-ops-cli
COPY ./ /opt/gitlab-ops-cli

WORKDIR /opt/gitlab-ops-cli

ENTRYPOINT [ "python", "run.py" ]
