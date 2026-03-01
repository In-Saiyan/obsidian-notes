---
tags:
  - devops
  - docker
  - networking
---

# Docker Networking

- [Network Drivers](#network-drivers)
- [Container DNS](#container-dns)
- [Common Patterns](#common-patterns)

---

## Network Drivers

| Driver | Description | Use Case |
|---|---|---|
| **bridge** | Default. Isolated network on a single host | Single-host containers communicating |
| **host** | Container shares the host's network stack | Performance-sensitive apps (no NAT overhead) |
| **none** | No networking | Batch jobs, security-sensitive tasks |
| **overlay** | Multi-host networking (Swarm / K8s) | Distributed applications |
| **macvlan** | Assigns a MAC address to the container | Legacy apps that expect to be on the LAN |

### Creating & Using a Custom Bridge Network

```bash
docker network create app-net

docker run -d --name api --network app-net my-api:1.0
docker run -d --name db  --network app-net postgres:16

# Containers on the same custom network can reach each other by name:
# api can connect to db using hostname "db"
```

---

## Container DNS

On **user-defined bridge networks**, Docker provides automatic DNS resolution:

- `<container-name>` resolves to the container's IP
- `<service-name>` in Compose resolves to any container of that service

> **Note:** The default `bridge` network does **not** support DNS resolution — use `--link` (deprecated) or create a custom network.

---

## Common Patterns

### Expose to Host Only

```bash
docker run -p 127.0.0.1:8080:80 nginx   # only accessible from localhost
```

### Inter-Container Communication Without Publishing Ports

Containers on the same network can talk over any port without `-p`:

```bash
docker network create internal
docker run -d --name redis --network internal redis:7
docker run -d --name app   --network internal my-app:1.0
# app can reach redis:6379 — no port publishing needed
```

### Isolating Frontend & Backend

```yaml
# compose.yaml
services:
  frontend:
    networks: [frontend]
  api:
    networks: [frontend, backend]
  db:
    networks: [backend]

networks:
  frontend:
  backend:
```

The `frontend` service **cannot** reach `db` directly — only `api` bridges both networks.
