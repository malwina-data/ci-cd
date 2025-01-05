source /home/ubuntu/app/myenv/bin/activate
pip install flask
nohup python3 main.py > main.log 2>&1 &
