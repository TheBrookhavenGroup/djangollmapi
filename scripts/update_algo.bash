#!/usr/bin/env bash
source ~/.bash_profile
source ~/.bashrc
pyenv shell djangollmapi
pip uninstall -y binoculars_algo
pip install git+ssh://git@github.com/Binoculars-Crew/binoculars_algo.git
sudo systemctl restart gunicorn.service
sudo systemctl restart celery.service
sudo systemctl restart celeryserial.service
