#! /bin/bash

docker rm -f favorites-service
docker build -t favorites-service .
docker run -d -p 8001:8001 --name favorites-service favorites-service
