FROM python:3.9-slim-bullseye

RUN apt update && \
    apt install vim unzip -y

COPY ./requirements.txt /tmp/

RUN python -m pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --upgrade -r /tmp/requirements.txt
#cli files
RUN mkdir /opt/gitlab-ops-cli
COPY ./ /opt/gitlab-ops-cli

WORKDIR /opt/gitlab-ops-cli

ENTRYPOINT [ "python", "run.py" ]
