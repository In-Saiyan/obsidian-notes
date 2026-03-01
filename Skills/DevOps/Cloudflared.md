# Cloudflared (Cloudflare Tunnel)

Cloudflare Tunnel (`cloudflared`) exposes local services to the internet **without opening inbound ports** or configuring firewall rules. Traffic routes through Cloudflare's network.

- [How It Works](#how-it-works)
- [Installation](#installation)
- [Quick Tunnel (no config)](#quick-tunnel-no-config)
- [Named Tunnel Setup](#named-tunnel-setup)
- [Configuration File](#configuration-file)
- [Running as a Service](#running-as-a-service)
- [Common Use Cases](#common-use-cases)

---

## How It Works

```
User → Cloudflare Edge → Cloudflare Tunnel → cloudflared (your server) → local service
```

- **No public IP needed** — cloudflared creates an outbound-only connection
- **No port forwarding** — nothing exposed on your firewall
- **DDoS protection** — traffic goes through Cloudflare
- **Zero Trust** — can add authentication via Cloudflare Access

---

## Installation

```bash
# Debian/Ubuntu
curl -fsSL https://pkg.cloudflare.com/cloudflare-main.gpg | sudo tee /usr/share/keyrings/cloudflare-main.gpg >/dev/null
echo "deb [signed-by=/usr/share/keyrings/cloudflare-main.gpg] https://pkg.cloudflare.com/cloudflared $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/cloudflared.list
sudo apt update && sudo apt install cloudflared

# Arch
yay -S cloudflared

# macOS
brew install cloudflared

# Docker
docker run cloudflare/cloudflared:latest tunnel --no-autoupdate run --token <TOKEN>
```

---

## Quick Tunnel (no config)

Instantly expose a local service with a random `*.trycloudflare.com` URL:

```bash
cloudflared tunnel --url http://localhost:3000
```

Good for testing. URL changes every time.

---

## Named Tunnel Setup

### 1. Authenticate

```bash
cloudflared tunnel login
# Opens browser → select your Cloudflare zone → saves cert to ~/.cloudflared/cert.pem
```

### 2. Create a Tunnel

```bash
cloudflared tunnel create my-tunnel
# Creates tunnel and saves credentials JSON in ~/.cloudflared/
```

### 3. Add DNS Record

```bash
cloudflared tunnel route dns my-tunnel app.example.com
# Creates a CNAME record pointing to the tunnel
```

### 4. Run

```bash
cloudflared tunnel run my-tunnel
```

---

## Configuration File

`~/.cloudflared/config.yml`

```yaml
tunnel: <TUNNEL_UUID>
credentials-file: /home/user/.cloudflared/<TUNNEL_UUID>.json

ingress:
  # Route app.example.com to local web server
  - hostname: app.example.com
    service: http://localhost:3000

  # Route api.example.com to a different service
  - hostname: api.example.com
    service: http://localhost:8080

  # SSH access
  - hostname: ssh.example.com
    service: ssh://localhost:22

  # Catch-all (required)
  - service: http_status:404
```

Then run with:

```bash
cloudflared tunnel run
```

---

## Running as a Service

```bash
# Install as systemd service
sudo cloudflared service install

# Or manually
sudo cloudflared --config /etc/cloudflared/config.yml tunnel run

# Enable on boot
sudo systemctl enable cloudflared
sudo systemctl start cloudflared
sudo systemctl status cloudflared
```

---

## Common Use Cases

| Use Case | Config |
|---|---|
| **Web app** | `service: http://localhost:3000` |
| **SSH** | `service: ssh://localhost:22` + Cloudflare Access |
| **RDP** | `service: rdp://localhost:3389` |
| **Minecraft server** | `service: tcp://localhost:25565` |
| **Self-hosted services** | Expose Gitea, Nextcloud, Home Assistant, etc. |
| **Development** | Quick tunnel for webhook testing |

---

## Useful Commands

```bash
cloudflared tunnel list                  # List all tunnels
cloudflared tunnel info my-tunnel        # Tunnel details
cloudflared tunnel delete my-tunnel      # Delete a tunnel
cloudflared tunnel route dns my-tunnel host.example.com  # Add DNS route
cloudflared tunnel route ip add 10.0.0.0/8 my-tunnel     # Route IP range
cloudflared access tcp --hostname ssh.example.com --url localhost:2222  # Client-side proxy
```
