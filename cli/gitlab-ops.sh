#!/usr/bin/env bash

if (! docker stats --no-stream >/dev/null 2>&1)
    then
        $START_DOCKER
while (! docker stats --no-stream >/dev/null 2>&1)
    do
        echo "Docker is launching"
        sleep 3
    done
fi

if [[ "$(docker images -q gitlab-ops-cli:latest 2>/dev/null)" != "" ]]
    then
        echo "Docker image exists"
else
    echo "Docker image doesn't exist."
    if [ ! $# -eq 0 ]
        then
            echo "Building..."
            if [ "$1" == "init" ]
                then
                    docker build -t gitlab-ops-cli .
            else
                docker build -t gitlab-ops-cli "$1"
            fi
    else
        echo "Run gitlab-ops in cli Dockerfile's path or "
        echo "Run gitlab-ops with path e.g., gitlab-ops /home/user/gitlab-ops/cli"
        docker build -t gitlab-ops-cli .
    fi
fi
echo
docker run --name gitlab-ops-cli -v /var/lib/gitlab-ops/.env:/opt/gitlab-ops-cli/.env --rm -it gitlab-ops-cli
