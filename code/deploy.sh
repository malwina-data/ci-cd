#!/bin/bash

# 1. Zainstaluj virtualenv, jeśli nie jest zainstalowany
sudo apt-get update
sudo apt-get install python3-venv

# 2. Utwórz środowisko wirtualne w folderze aplikacji
python3 -m venv /home/ubuntu/app/venv

# 3. Aktywuj środowisko wirtualne
source /home/ubuntu/app/venv/bin/activate

# 4. Zainstaluj zależności w środowisku wirtualnym
pip install -r /home/ubuntu/app/requirements.txt

# 5. Uruchom aplikację w tle przy użyciu nohup (bez logów)
nohup python3 /home/ubuntu/app/main.py &


