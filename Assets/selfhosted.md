---
tags:
  - assets
  - selfhosted
  - docker
  - docker-compose
---

# Useful SelfHosted

> [!DANGER]
> PLEASE BIND THE PORTS TO 127.0.0.1 if you are running it on a VPS with IP exposed to the world... 

> [!WARNING]
> SSL certs carry information you can use default certs from cloudflare by setting TLS flexible and just routing the raw traffic without 2 way SSL to be more anonymous.

# Media Stack
## Jellyfin + *Arrs
```yaml
services:
  prowlarr:
    image: lscr.io/linuxserver/prowlarr:latest
    container_name: prowlarr
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Asia/Kolkata
    volumes:
      - ./prowlarr/config:/config
    ports:
      - 127.0.0.1:9696:9696
    restart: unless-stopped
    networks: [mediaservarr]

  sonarr:
    image: lscr.io/linuxserver/sonarr:latest
    container_name: sonarr
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Asia/Kolkata
    volumes:
      - ./sonarr/config:/config
      - ./media/tvseries:/tv
      - ./downloads:/downloads
    ports:
      - 127.0.0.1:8989:8989
    restart: unless-stopped
    networks: [mediaservarr]
    depends_on: [qbittorrent, prowlarr]

  radarr:
    image: lscr.io/linuxserver/radarr:latest
    container_name: radarr
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Asia/Kolkata
    volumes:
      - ./radarr/config:/config
      - ./media/movies:/movies
      - ./downloads:/downloads
    ports:
      - 127.0.0.1:7878:7878
    restart: unless-stopped
    networks: [mediaservarr]
    depends_on: [qbittorrent, prowlarr]

  bazarr:
    image: lscr.io/linuxserver/bazarr:latest
    container_name: bazarr
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Asia/Kolkata
    volumes:
      - ./bazarr/config:/config
      - ./media/tvseries:/tv
      - ./media/movies:/movies
    ports:
      - 127.0.0.1:6767:6767
    restart: unless-stopped
    networks: [mediaservarr]
    depends_on: [sonarr, radarr]

  jellyfin:
    image: lscr.io/linuxserver/jellyfin:latest
    container_name: jellyfin
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Asia/Kolkata
      - JELLYFIN_PublishedServerUrl=https://jellyfin.yukihana.app
    volumes:
      - ./jellyfin/config:/config
      - ./media/tvseries:/data/tvshows
      - ./media/movies:/data/movies
      - ./media/music:/data/music
    ports:
      - 127.0.0.1:8096:8096
      # UDP ports usually need to remain unbound or bound to 0.0.0.0 for DLNA to work on LAN.
      # If you don't use DLNA casting, you can bind them to 127.0.0.1 or remove them.
      - 8920:8920
      - 7359:7359/udp
      - 1900:1900/udp
    restart: unless-stopped
    networks: [mediaservarr]

  jellyseerr:
    image: fallenbagel/jellyseerr:latest
    container_name: jellyseerr
    environment:
      - TZ=Asia/Kolkata
      - LOG_LEVEL=debug
      - PORT=5055
    volumes:
      - ./jellyseerr/config:/app/config
    ports:
      - 127.0.0.1:5055:5055
    restart: unless-stopped
    networks: [mediaservarr]
    depends_on: [jellyfin]

  flaresolverr:
    image: ghcr.io/flaresolverr/flaresolverr:latest
    container_name: flaresolverr
    environment:
      - LOG_LEVEL=info
    volumes:
      - ./flaresolverr/config:/config
    ports:
      - 127.0.0.1:8191:8191
    restart: unless-stopped
    networks: [mediaservarr]

  qbittorrent:
    image: lscr.io/linuxserver/qbittorrent:latest
    container_name: qbittorrent
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Asia/Kolkata
      - WEBUI_PORT=8080
      - TORRENTING_PORT=6881
    volumes:
      - ./qbittorrent/config:/config
      - ./downloads:/downloads
    ports:
      - 127.0.0.1:8080:8080
      # Torrenting ports MUST be exposed to the world (0.0.0.0) to work
      - 6881:6881
      - 6881:6881/udp
    restart: unless-stopped
    networks: [mediaservarr]

  slskd:
    image: slskd/slskd:latest
    container_name: slskd
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Asia/Kolkata
      # --- DASHBOARD LOGIN ---
      - SLSKD_USERNAME=red
      - SLSKD_PASSWORD=red
      # Only keep this if you want to force this specific key on startup:
      - SLSKD_API_KEY=redred
      # -----------------------

      # --- SOULSEEK LOGIN ---
      - SLSKD_SLSK_USERNAME=red
      - SLSKD_SLSK_PASSWORD=red
      # ----------------------

      - SLSKD_APP_DIR=/app/config
      - SLSKD_DOWNLOADS_DIR=/music/soulseek
      - SLSKD_INCOMPLETE_DIR=/downloads/slskd_incomplete
      - SLSKD_SHARED_DIR=/music
    volumes:
      - ./slskd/config:/app/config
      - ./downloads:/downloads
      - ./media/music:/music
    ports:
      - 127.0.0.1:5030:5030
      # Soulseek transfer ports MUST be exposed to the world (0.0.0.0)
      - 50300:50300
    restart: unless-stopped
    networks: [mediaservarr]

  navidrome:
    image: deluan/navidrome:latest
    container_name: navidrome
    user: 1000:1000
    environment:
      - ND_SCANSCHEDULE=1h
      - ND_LOGLEVEL=info
      - ND_SESSIONTIMEOUT=24h
    volumes:
      - ./navidrome/data:/data
      - ./media/music:/music:ro
    ports:
      - 127.0.0.1:4533:4533
    restart: unless-stopped
    networks: [mediaservarr]

  watchtower:
    image: containrrr/watchtower
    container_name: watchtower
    environment:
      - LOG_LEVEL=info
      - DOCKER_API_VERSION=1.45
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    command: --interval 30
    restart: unless-stopped

networks:
  mediaservarr:
    driver: bridge
```

# Backrest
Backup service for VPS

> [!NOTE]
> Also save a config inside `./rclone/rclone.conf`

```yaml
services:
  backrest:
    image: garethgeorge/backrest:latest
    container_name: backrest
    restart: unless-stopped
    # Use host networking or specific port binding.
    # Since you want 127.0.0.1 specifically:
    ports:
      - "127.0.0.1:9898:9898"
    environment:
      - TZ=Asia/Kolkata  # Adjust timezone if needed
      # BACKREST_PORT=0.0.0.0:9898 # Internal bind (leave default)
      # PUID=1000 # Uncomment and match your user ID if you want file permissions to match yours
      # PGID=1000
    volumes:
      # Persistent data for Backrest (Database, binary cache, etc)
      - ./data:/data
      - ./config:/config
      - ./cache:/cache

      # MOUNT: Your Music Folder
      # We mount it to /source/music so it's easy to find in the UI.
      # :ro makes it Read-Only (safety best practice for backups)
      - /home/ryan/opt/mediaservarr/media/music:/source/music:ro

      # MOUNT: Rclone Config
      # Backrest uses Rclone for Google Drive. You need to map the config file.
      # See instructions below on how to generate this.
      - ./rclone:/root/.config/rclone
```

# Dockhand
Docker Management tool(WebUI)
```yaml
❯ altcat docker-compose.yml
services:
  postgres:
    image: postgres:16
    environment:
      POSTGRES_USER: red
      POSTGRES_PASSWORD: red
      POSTGRES_DB: red
    volumes:
      - postgres_data:/var/lib/postgresql/data

  dockhand:
    image: fnsys/dockhand:latest
    ports:
      - 127.0.0.1:3000:3000
    environment:
      # FIX 1: Use dashes (-) for ALL environment variables
      - DATABASE_URL=postgres://red:red@postgres:5432/red
      - PUID=1000
      - PGID=1000
    volumes:
      # FIX 2: Fixed indentation (was 3 spaces, needs to match 'environment')
      - /var/run/docker.sock:/var/run/docker.sock
      - dockhand_data:/app/data
      - /home/ryan/opt:/home/ryan/opt
    depends_on:
      - postgres

volumes:
  postgres_data:
  dockhand_data:
```

# Gitea
Personal Github?

```yaml
version: "3"

networks:
  gitea:
    external: false

services:
  server:
    image: gitea/gitea:latest
    container_name: gitea
    environment:
      - USER_UID=1000
      - USER_GID=1000
      - GITEA__database__DB_TYPE=red
      - GITEA__database__HOST=db:5432
      - GITEA__database__NAME=red
      - GITEA__database__USER=red
      - GITEA__database__PASSWD=red
    restart: always
    networks:
      - gitea
    volumes:
      - ./gitea:/data
      - /etc/timezone:/etc/timezone:ro
      - /etc/localtime:/etc/localtime:ro
    ports:
      - "127.0.0.1:3696:3000"
      - "127.0.0.1:222:22"
    depends_on:
      - db

  db:
    image: postgres:15-alpine
    restart: always
    container_name: gitea_db
    environment:
      - POSTGRES_USER=red
      - POSTGRES_PASSWORD=red
      - POSTGRES_DB=red
    networks:
      - gitea
    volumes:
      - ./postgres:/var/lib/postgresql/data
```

