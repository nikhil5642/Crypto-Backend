#! /bin/bash

pkill gunicorn &
kill -9 `ps aux | grep gunicorn | awk '{print $2}'` &
pkill -f server.fastApi.service 
