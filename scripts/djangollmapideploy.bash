#!/usr/bin/env bash

cd djangollmapi
source ~/.bash_profile
source ~/.bashrc
pyenv shell djangollmapi
git pull
python manage.py migrate
sudo systemctl restart gunicorn.service
sudo systemctl restart celery.service
sudo systemctl restart celeryserial.service
