#! /bin/bash

docker rm -f favorites-service favorites-mongodb
docker run -d -p 27017:27017 --name favorites-mongodb mongo
docker build -t favorites-service .
docker run -d -p 8000:8000 --name favorites-service favorites-service
