#!/usr/bin/env bash

if [ $# -eq 0 ] || [ "$1" == linux ]
    then
        if [ ! -d "/var/lib/gitlab-ops/" ]
            then
                sudo mkdir /var/lib/gitlab-ops/
        fi
        ABS_PATH=$(dirname "$(realpath "$0")")
        sudo cp "$ABS_PATH"/.env /var/lib/gitlab-ops/.env
        export START_DOCKER="systemctl start docker"
elif [ "$1" == mac ]
    then
        if [ ! -d "/var/lib/gitlab-ops/" ]
        then
            sudo mkdir /var/lib/gitlab-ops/
        fi
        ABS_PATH=$(dirname "$(realpath "$0")")
        sudo cp "$ABS_PATH"/.env /var/lib/gitlab-ops/.env
        export START_DOCKER="open /Applications/Docker.app"
else
    echo "not supported"
    exit
fi

envsubst < "$ABS_PATH"/gitlab-ops.sh > /usr/local/bin/gitlab-ops
sudo chmod +x /usr/local/bin/gitlab-ops

gitlab-ops init