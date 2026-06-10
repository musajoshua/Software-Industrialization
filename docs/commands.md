# Docker Commands

```bash
docker inspect <container name>
```

```bash
docker network create <name>
```

```bash
docker network rm <name>
```

```bash
docker network inspect <network name>
```

```bash
docker network connect <network name> <container name>
```

```bash
docker network disconnect <network name> <container name>
```

```bash
docker network ls
```

```bash
docker volume ls
```

```bash
docker ... -v <name>:/var/lib/mysql
```

```bash
docker run -d --name <name of container> --network <network name> -e MYSQL_ROOT_PASSWORD=root -e MYSQL_ROOT_HOST=% -v mysql2-data:/var/lib/mysql mysql:latest
```

networks in docker

- Bridge
- "None"
- Host
- Overlay -> docker swam

## Docker compose

```bash
docker compose up - d
docker compose down - d
```
