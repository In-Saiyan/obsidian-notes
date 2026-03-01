---
tags:
  - devops
  - docker
  - containers
---

# Docker Basics

- [What is Docker?](#what-is-docker)
- [Docker vs Virtual Machines](#docker-vs-virtual-machines)
- [Core Concepts](#core-concepts)
- [Docker Architecture](#docker-architecture)
- [Image Lifecycle](#image-lifecycle)
- [Container Lifecycle](#container-lifecycle)
- [Essential Commands](#essential-commands)

---

## What is Docker?

Docker is a platform for **building, shipping, and running** applications inside lightweight, portable **containers**. A container packages an application with all its dependencies so it runs consistently across any environment.

**Why Docker?**
- **Consistency** — "works on my machine" is eliminated
- **Isolation** — each container has its own filesystem, network, and process space
- **Speed** — containers start in seconds (no OS boot)
- **Portability** — runs on any machine with Docker installed
- **Efficiency** — shares the host kernel; far lighter than VMs

---

## Docker vs Virtual Machines

| | Docker Container | Virtual Machine |
|---|---|---|
| **Virtualisation** | OS-level (shares host kernel) | Hardware-level (full guest OS) |
| **Startup** | Seconds | Minutes |
| **Size** | MBs | GBs |
| **Performance** | Near-native | Overhead from hypervisor |
| **Isolation** | Process-level | Full OS-level |
| **Use case** | Microservices, CI/CD | Full OS environments, legacy apps |

---

## Core Concepts

| Concept | Description |
|---|---|
| **Image** | Read-only template with application code, runtime, libraries, and config |
| **Container** | A running instance of an image |
| **Dockerfile** | Text file with instructions to build an image |
| **Registry** | Storage service for images (Docker Hub, ECR, GCR, ACR) |
| **Volume** | Persistent storage that outlives the container |
| **Network** | Virtual network that connects containers |

---

## Docker Architecture

Docker uses a **client-server** model:

```
┌──────────┐       REST API       ┌──────────────┐
│  Docker   │ ──────────────────▶ │  Docker       │
│  CLI      │                     │  Daemon       │
│  (client) │ ◀────────────────── │  (dockerd)    │
└──────────┘                     └──────┬───────┘
                                        │
                              ┌─────────┴─────────┐
                              │    containerd      │
                              │  (container runtime)│
                              └─────────┬─────────┘
                                        │
                              ┌─────────┴─────────┐
                              │      runc          │
                              │  (OCI runtime)     │
                              └───────────────────┘
```

- **Docker CLI** — user-facing command-line tool
- **Docker Daemon (dockerd)** — manages images, containers, networks, volumes
- **containerd** — high-level container runtime
- **runc** — low-level OCI runtime that creates containers

---

## Image Lifecycle

```bash
# Pull an image from a registry
docker pull nginx:1.27

# List local images
docker images

# Build an image from a Dockerfile
docker build -t myapp:1.0 .

# Tag an image
docker tag myapp:1.0 registry.example.com/myapp:1.0

# Push to a registry
docker push registry.example.com/myapp:1.0

# Remove an image
docker rmi myapp:1.0

# Prune unused images
docker image prune -a
```

---

## Container Lifecycle

```
Created → Running → Paused → Running → Stopped → Removed
```

```bash
# Run a container (pull + create + start)
docker run -d --name web -p 8080:80 nginx:1.27

# List running containers
docker ps

# List all containers (including stopped)
docker ps -a

# Stop a running container
docker stop web

# Start a stopped container
docker start web

# Restart
docker restart web

# Remove a stopped container
docker rm web

# Force remove a running container
docker rm -f web

# View logs
docker logs web -f --tail 50

# Execute a command inside a running container
docker exec -it web /bin/sh

# Inspect container details
docker inspect web
```

---

## Essential Commands

### System

```bash
docker info                    # System-wide information
docker version                 # Client and server versions
docker system df               # Disk usage
docker system prune -a         # Remove all unused data
```

### Networking

```bash
docker network ls              # List networks
docker network create mynet    # Create a custom network
docker network inspect mynet   # Inspect network details
docker run --network mynet ... # Attach container to network
```

### Volumes

```bash
docker volume ls               # List volumes
docker volume create mydata    # Create a named volume
docker volume inspect mydata   # Inspect volume
docker run -v mydata:/app/data ... # Mount volume into container
docker volume rm mydata        # Remove volume
```
