#!/bin/bash
docker compose down
docker system prune -y
docker volume rm irnusdl_static_volume
docker compose up --build -d
