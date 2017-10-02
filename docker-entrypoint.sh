#!/bin/bash
rsync -rv /usr/src/app_original/ /usr/src/app/ \
    --exclude=__pycache__ \
    --exclude=.git \
    --exclude=.idea \
    --exclude=htmlcov \
    --exclude=*.egg-info
exec "$@"