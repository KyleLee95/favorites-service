#! /bin/bash

docker rm -f favorites-service favorites-mongodb
docker run -d -p 27017:27017 --name favorites-mongodb mongo
docker compose up --build
