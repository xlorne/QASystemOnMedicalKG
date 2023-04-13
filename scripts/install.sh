docker-compose -f server.yaml build --no-cache
docker-compose -f server.yaml up -d
docker ps -a