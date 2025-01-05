#!/bin/bash

# 1. Zainstaluj virtualenv, jeśli nie jest zainstalowany
sudo apt-get update
sudo apt-get install python3-venv

# 2. Utwórz środowisko wirtualne w folderze aplikacji
python3 -m venv /home/ubuntu/app/venv

# 3. Aktywuj środowisko wirtualne
source /home/ubuntu/app/venv/bin/activate

# 4. Zainstaluj gunicorn
pip install flask
pip install gunicorn

nohup gunicorn -w 1 -b 0.0.0.0:5000 main:app > gunicorn.log 2>&1 &
