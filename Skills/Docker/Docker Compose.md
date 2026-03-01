# Docker Compose

Docker Compose is a tool for defining and running **multi-container** applications using a single YAML file.

- [Basic Structure](#basic-structure)
- [Common Configuration](#common-configuration)
- [Commands](#commands)
- [Example — Full Stack App](#example-full-stack-app)

---

## Basic Structure

```yaml
# compose.yaml (v2+ uses this filename)
services:
  web:
    image: nginx:1.27
    ports:
      - "8080:80"
  db:
    image: postgres:16
    environment:
      POSTGRES_PASSWORD: secret
```

---

## Common Configuration

| Key | Purpose | Example |
|---|---|---|
| `image` | Use a pre-built image | `image: redis:7` |
| `build` | Build from Dockerfile | `build: ./app` |
| `ports` | Map host:container ports | `ports: ["3000:3000"]` |
| `environment` | Set env vars | `environment: { DB: postgres }` |
| `env_file` | Load env from file | `env_file: .env` |
| `volumes` | Mount volumes | `volumes: ["./data:/var/lib/data"]` |
| `depends_on` | Start order | `depends_on: [db]` |
| `networks` | Attach to networks | `networks: [backend]` |
| `restart` | Restart policy | `restart: unless-stopped` |
| `healthcheck` | Health check | `healthcheck: { test: ["CMD", "curl", "-f", "http://localhost"] }` |

---

## Commands

```bash
# Start all services (detached)
docker compose up -d

# Stop and remove containers, networks
docker compose down

# Rebuild images
docker compose build

# View logs
docker compose logs -f web

# Scale a service
docker compose up -d --scale worker=3

# List running services
docker compose ps

# Execute command in a service
docker compose exec web sh
```

---

## Example — Full Stack App

```yaml
services:
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - api

  api:
    build: ./api
    ports:
      - "8080:8080"
    environment:
      DATABASE_URL: postgres://user:pass@db:5432/app
    depends_on:
      db:
        condition: service_healthy

  db:
    image: postgres:16
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: app
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user"]
      interval: 5s
      retries: 5

volumes:
  pgdata:
```
