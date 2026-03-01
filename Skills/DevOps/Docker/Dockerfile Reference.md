---
tags:
  - devops
  - docker
  - dockerfile
---

# Dockerfile Reference

A **Dockerfile** is a text file containing ordered instructions to assemble a Docker image.

- [Basic Structure](#basic-structure)
- [Common Instructions](#common-instructions)
- [Multi-Stage Builds](#multi-stage-builds)
- [Best Practices](#best-practices)

---

## Basic Structure

```dockerfile
# syntax=docker/dockerfile:1
FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --production

COPY . .

EXPOSE 3000
CMD ["node", "server.js"]
```

---

## Common Instructions

| Instruction | Purpose | Example |
|---|---|---|
| `FROM` | Base image | `FROM python:3.12-slim` |
| `WORKDIR` | Set working directory | `WORKDIR /app` |
| `COPY` | Copy files from build context | `COPY . .` |
| `ADD` | Like COPY but supports URLs and tar extraction | `ADD app.tar.gz /app` |
| `RUN` | Execute command during build | `RUN apt-get update && apt-get install -y curl` |
| `ENV` | Set environment variable | `ENV NODE_ENV=production` |
| `ARG` | Build-time variable | `ARG VERSION=1.0` |
| `EXPOSE` | Document the port the container listens on | `EXPOSE 8080` |
| `CMD` | Default command when container starts | `CMD ["python", "app.py"]` |
| `ENTRYPOINT` | Fixed command (CMD becomes arguments) | `ENTRYPOINT ["java", "-jar"]` |
| `VOLUME` | Create a mount point | `VOLUME /data` |
| `USER` | Set the user for subsequent instructions | `USER appuser` |
| `HEALTHCHECK` | Container health check | `HEALTHCHECK CMD curl -f http://localhost/` |

---

## Multi-Stage Builds

Reduce final image size by separating build and runtime stages:

```dockerfile
# --- Build stage ---
FROM golang:1.22 AS builder
WORKDIR /src
COPY . .
RUN CGO_ENABLED=0 go build -o /app

# --- Runtime stage ---
FROM alpine:3.19
COPY --from=builder /app /app
ENTRYPOINT ["/app"]
```

**Benefits:**
- Build tools and source code are **not** included in the final image
- Dramatically smaller images (e.g. 800 MB → 15 MB)

---

## Best Practices

1. **Use specific base image tags** — `node:20-alpine` not `node:latest`
2. **Minimise layers** — combine related `RUN` commands with `&&`
3. **Order instructions by change frequency** — put rarely-changing steps first for better caching
4. **Use `.dockerignore`** — exclude `node_modules`, `.git`, build artifacts
5. **Don't run as root** — add `USER appuser` after creating the user
6. **Use multi-stage builds** — separate build and runtime dependencies
7. **Scan images** — `docker scout cves <image>` or Trivy
