#! /bin/bash

docker rm -f favorites-service
docker build -t favorites-service .
docker run -d -p 8000:8000 --name favorites-service favorites-service
