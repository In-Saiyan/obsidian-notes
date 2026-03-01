# Docker Volumes & Storage

- [[#Storage Types]]
- [[#Volumes]]
- [[#Bind Mounts]]
- [[#tmpfs Mounts]]
- [[#Backup & Restore]]

---

## Storage Types

| Type | Managed by Docker? | Persists after container removal? | Use Case |
|---|---|---|---|
| **Volume** | Yes | Yes | Databases, stateful apps |
| **Bind Mount** | No (host path) | Yes | Development (live reload) |
| **tmpfs** | No (RAM) | No | Sensitive data, scratch space |

---

## Volumes

Volumes are the **preferred** way to persist data.

```bash
# Create
docker volume create mydata

# Mount into container
docker run -d -v mydata:/var/lib/data myapp:1.0

# Inspect
docker volume inspect mydata

# List
docker volume ls

# Remove
docker volume rm mydata

# Prune unused volumes
docker volume prune
```

### Named Volume in Compose

```yaml
services:
  db:
    image: postgres:16
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:   # Docker manages this
```

---

## Bind Mounts

Map a **specific host directory** into the container. Commonly used for development.

```bash
docker run -d -v $(pwd)/src:/app/src myapp:1.0
```

```yaml
# Compose
services:
  app:
    volumes:
      - ./src:/app/src   # host path : container path
```

> **Warning:** Bind mounts expose host filesystem — avoid in production.

---

## tmpfs Mounts

Data stored in **memory only**; never written to the host filesystem.

```bash
docker run -d --tmpfs /tmp:rw,size=64m myapp:1.0
```

Use cases: caching, secrets that should not persist on disk.

---

## Backup & Restore

### Backup a Volume

```bash
docker run --rm \
  -v mydata:/data \
  -v $(pwd):/backup \
  busybox tar czf /backup/mydata-backup.tar.gz -C /data .
```

### Restore a Volume

```bash
docker run --rm \
  -v mydata:/data \
  -v $(pwd):/backup \
  busybox tar xzf /backup/mydata-backup.tar.gz -C /data
```
