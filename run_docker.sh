docker container rm /amtrak || true
docker run --publish 3000:3000 --detach --name amtrak --restart unless-stopped ghcr.io/jwoglom/amtrak-schedule-js:sha-54fa3fa --webui
