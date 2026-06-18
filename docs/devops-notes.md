# DevOps Class Notes

A reference document covering everything done so far — from running an app locally to deploying it with Docker Compose on a cloud VM.

---

## Table of Contents

1. [Running the App Locally](#1-running-the-app-locally)
2. [Setting Up a VM on Azure](#2-setting-up-a-vm-on-azure)
3. [Pushing to GitHub & Running on the VM](#3-pushing-to-github--running-on-the-vm)
4. [Docker Basics](#4-docker-basics)
5. [Running Docker on the VM](#5-running-docker-on-the-vm)
6. [Docker Networking](#6-docker-networking)
7. [Inspecting Docker Objects](#7-inspecting-docker-objects)
8. [Pushing Images to Docker Hub](#8-pushing-images-to-docker-hub)
9. [Switching to Docker Compose](#9-switching-to-docker-compose)
10. [Running Docker Compose on the VM](#10-running-docker-compose-on-the-vm)
11. [Cheatsheet](#cheatsheet)

---

## 1. Running the App Locally

The starting point was a bootstrapped Python app used as a test subject throughout the course.

**What "running locally" means:** the app runs directly on your machine using your local Python environment — no containers, no cloud, no VM.

**Typical steps:**
```bash
# Clone or unzip the project
cd your-app/

# (Optional) create a virtual environment
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

> **Why this matters:** before automating or containerizing anything, you need to confirm the app actually works. This also helps you understand what the app needs (env vars, ports, a database, etc.).

---

## 2. Setting Up a VM on Azure

A **Virtual Machine (VM)** is a computer running in the cloud. Azure provisions it for you — you get an IP address and can connect to it like a remote computer.

**Steps:**
1. Create a VM in the Azure portal (choose Ubuntu, pick a size)
2. During setup, Azure generates an SSH key pair — download the `.pem` private key
3. Open port 22 (SSH) in the VM's network security group

**Connecting via SSH:**
```bash
# Give correct permissions to your key file (Linux/Mac only)
chmod 400 your-key.pem

# Connect
ssh -i your-key.pem azureuser@<VM_PUBLIC_IP>
```

> **SSH (Secure Shell):** a protocol that lets you remotely control another machine via the terminal. You authenticate with a key file instead of a password.

---

## 3. Pushing to GitHub & Running on the VM

The goal here was to get the app's code from your local machine onto the VM, using GitHub as the middleman.

**Local → GitHub:**
```bash
git init
git add .
git commit -m "initial commit"
git remote add origin https://github.com/your-username/your-repo.git
git push -u origin main
```

**GitHub → VM (inside the VM via SSH):**
```bash
# Install git if needed
sudo apt update && sudo apt install git -y

# Clone the repo
git clone https://github.com/your-username/your-repo.git
cd your-repo

# Install Python deps and run
pip install -r requirements.txt
python app.py
```

> **Why not copy files directly?** GitHub gives you version control, a clean transfer method, and makes future updates easy — just `git pull` on the VM.

---

## 4. Docker Basics

**Docker** lets you package an application and everything it needs (code, runtime, libraries) into a **container** — an isolated, portable unit that runs the same everywhere.

### Key Concepts

| Concept | Description |
|---|---|
| **Image** | A blueprint/template for a container (read-only) |
| **Container** | A running instance of an image |
| **Dockerfile** | A script that defines how to build a custom image |
| **Volume** | Persistent storage that survives container restarts |
| **Registry** | A place to store and share images (e.g. Docker Hub) |

### Dockerfile Example
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000
CMD ["python", "app.py"]
```

### Running a pre-built image (e.g. MySQL)
```bash
docker run -d \
  --name mysql-container \
  -e MYSQL_ROOT_PASSWORD=secret \
  -e MYSQL_DATABASE=mydb \
  -p 3306:3306 \
  mysql:8
```

- `-d` — detached mode (runs in background)
- `--name` — give the container a name
- `-e` — set environment variables
- `-p host:container` — map a port on your machine to a port in the container

---

## 5. Running Docker on the VM

Same Docker commands, but executed inside the VM (after SSH-ing in).

**Install Docker on the VM:**
```bash
sudo apt update
sudo apt install docker.io -y
sudo systemctl start docker
sudo systemctl enable docker

# Allow your user to run docker without sudo
sudo usermod -aG docker $USER
# Then log out and back in for the group change to apply
```

**Then run your images the same way as locally.**

> **Why run on the VM?** Your local machine isn't always on. The VM runs 24/7 and has a public IP, so your app is actually accessible from anywhere.

---

## 6. Docker Networking

By default, containers are isolated. A **Docker network** lets containers talk to each other by name.

### Create a private network
```bash
docker network create my-network
```

### Attach containers to the network
```bash
docker run -d --name app --network my-network my-app-image
docker run -d --name db --network my-network mysql:8
```

Now the `app` container can reach the database using `db` as the hostname (instead of an IP address).

### Network types

| Type | Description |
|---|---|
| `bridge` | Default. Isolated network on a single host |
| `host` | Container shares the host's network stack |
| `none` | No networking |

---

## 7. Inspecting Docker Objects

Useful commands for understanding what's running and how it's configured.

```bash
# List running containers
docker ps

# List all containers (including stopped)
docker ps -a

# List images
docker images

# List networks
docker network ls

# List volumes
docker volume ls

# Detailed info on anything (container, image, network, volume)
docker inspect <name-or-id>

# View logs of a container
docker logs <container-name>

# Get a shell inside a running container
docker exec -it <container-name> bash
```

---

## 8. Pushing Images to Docker Hub

Docker Hub is the default public registry. You can push your own images there so they can be pulled from anywhere (like a VM).

### Steps

```bash
# 1. Log in
docker login

# 2. Build your image
docker build -t my-app .

# 3. Tag it with your Docker Hub username and a version
docker tag my-app yourusername/my-app:v1

# 4. Push it
docker push yourusername/my-app:v1
```

> **Tags** are like version labels. `latest` is the default tag if you don't specify one. Using explicit versions (`v1`, `v2`) is better practice so you know exactly what's deployed.

### Pull it anywhere
```bash
docker pull yourusername/my-app:v1
```

---

## 9. Switching to Docker Compose

**Docker Compose** lets you define and run multi-container applications using a single `docker-compose.yml` file — instead of running long `docker run` commands manually.

### Example `docker-compose.yml`
```yaml
version: "3.9"

services:
  app:
    image: yourusername/my-app:v1
    ports:
      - "5000:5000"
    environment:
      - DB_HOST=db
      - DB_PASSWORD=secret
    depends_on:
      - db
    networks:
      - app-network

  db:
    image: mysql:8
    environment:
      MYSQL_ROOT_PASSWORD: secret
      MYSQL_DATABASE: mydb
    volumes:
      - db-data:/var/lib/mysql
    networks:
      - app-network

volumes:
  db-data:

networks:
  app-network:
```

### Key fields

| Field | Description |
|---|---|
| `image` | Which image to use (pulled from Docker Hub) |
| `ports` | Port mapping (`host:container`) |
| `environment` | Env variables passed to the container |
| `depends_on` | Start order (doesn't wait for readiness, just startup) |
| `volumes` | Mount persistent storage |
| `networks` | Which network(s) to attach to |

---

## 10. Running Docker Compose on the VM

Same process as locally — just SSH into the VM first, then use Compose.

```bash
# SSH in
ssh -i your-key.pem azureuser@<VM_PUBLIC_IP>

# Install Docker Compose (if not already installed)
sudo apt install docker-compose -y
# or for the newer plugin version:
sudo apt install docker-compose-plugin -y

# Go to your project folder (clone from GitHub if needed)
git clone https://github.com/your-username/your-repo.git
cd your-repo

# Start everything
docker compose up -d

# Check it's running
docker compose ps
```

> With Compose, your entire stack (app + database + network + volumes) comes up with one command. This is the foundation of how real deployments work.

---

## Cheatsheet

### Docker

```bash
# ── Images ──────────────────────────────────────────────
docker build -t name:tag .           # Build image from Dockerfile
docker images                        # List local images
docker rmi name:tag                  # Remove an image
docker pull name:tag                 # Pull image from registry
docker push name:tag                 # Push image to registry
docker tag source target             # Tag an image

# ── Containers ──────────────────────────────────────────
docker run -d --name c1 image        # Run container in background
docker run -it image bash            # Run container interactively
docker ps                            # List running containers
docker ps -a                         # List all containers
docker stop c1                       # Stop a container
docker start c1                      # Start a stopped container
docker rm c1                         # Remove a stopped container
docker rm -f c1                      # Force remove (even if running)
docker logs c1                       # View container logs
docker logs -f c1                    # Follow logs (live)
docker exec -it c1 bash              # Open shell inside container

# ── Networks ─────────────────────────────────────────────
docker network create my-net         # Create a network
docker network ls                    # List networks
docker network inspect my-net        # Inspect a network
docker network rm my-net             # Remove a network

# ── Volumes ──────────────────────────────────────────────
docker volume create my-vol          # Create a volume
docker volume ls                     # List volumes
docker volume inspect my-vol         # Inspect a volume
docker volume rm my-vol              # Remove a volume

# ── System cleanup ───────────────────────────────────────
docker system prune                  # Remove unused containers/images/networks
docker system prune -a               # Also remove unused images
```

### Docker Compose

```bash
# ── Lifecycle ────────────────────────────────────────────
docker compose up                    # Start all services (foreground)
docker compose up -d                 # Start all services (background)
docker compose up --build            # Rebuild images before starting
docker compose down                  # Stop and remove containers + networks
docker compose down -v               # Also remove volumes
docker compose restart               # Restart all services

# ── Monitoring ───────────────────────────────────────────
docker compose ps                    # List running services
docker compose logs                  # View logs for all services
docker compose logs -f               # Follow logs
docker compose logs app              # Logs for a specific service

# ── Running commands ─────────────────────────────────────
docker compose exec app bash         # Open shell in a running service
docker compose run app python shell  # Run a one-off command

# ── Images ───────────────────────────────────────────────
docker compose pull                  # Pull latest images defined in compose file
docker compose build                 # Build images defined in compose file
```

---

*Last updated: June 2026*
