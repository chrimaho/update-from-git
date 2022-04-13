docker compose `
    --file ./docker/docker-compose.yml `
    stop ;`
docker compose `
    --file ./docker/docker-compose.yml `
    down ;`
docker rmi $(docker images --all --quiet)