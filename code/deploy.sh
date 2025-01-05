source /home/ubuntu/app/myenv/bin/activate

nohup gunicorn -w 1 -b 0.0.0.0:5000 main:app > gunicorn.log 2>&1 &
