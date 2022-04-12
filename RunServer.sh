#! /bin/bash

pkill gunicorn &
kill -9 `ps aux | grep gunicorn | awk '{print $2}'` &
pkill -f server.fastApi.service
redis-server &
python3 -m server.fastApi.services &
gunicorn --bind 0.0.0.0:80 server.fastApi.app:app -w 4 -k uvicorn.workers.UvicornWorker &
