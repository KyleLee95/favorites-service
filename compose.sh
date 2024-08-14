#! /bin/bash

docker rm -f favorites-service favorites-mongodb
docker compose up --build
