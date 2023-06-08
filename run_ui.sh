docker container stop /amtrak-ui || true
docker container rm /amtrak-ui || true
docker run --publish 8000:8000 --detach --restart unless-stopped --name amtrak-ui -e DATA_FOLDER=/data -v /srv/amtrak/data:/data ghcr.io/jwoglom/amtrak-schedule-scrape-ui:sha-ef7c7bb