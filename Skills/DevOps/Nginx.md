---
tags:
  - devops
  - nginx
  - web-server
  - reverse-proxy
  - load-balancer
---

# Nginx

A high-performance **web server**, **reverse proxy**, and **load balancer**.

- [Installation](#installation)
- [File Structure](#file-structure)
- [Basic Config](#basic-config)
- [Serving Static Files](#serving-static-files)
- [Reverse Proxy](#reverse-proxy)
- [Load Balancing](#load-balancing)
- [SSL/TLS (HTTPS)](#ssltls-https)
- [Common Directives](#common-directives)
- [Useful Commands](#useful-commands)

---

## Installation

```bash
# Debian/Ubuntu
sudo apt update && sudo apt install nginx

# Arch
sudo pacman -S nginx

# macOS
brew install nginx

# Docker
docker run -d -p 80:80 nginx:1.27
```

---

## File Structure

```
/etc/nginx/
├── nginx.conf              # Main config
├── sites-available/        # Virtual host configs
│   └── default
├── sites-enabled/          # Symlinks to active configs
│   └── default → ../sites-available/default
├── conf.d/                 # Additional config fragments
└── snippets/               # Reusable config snippets
```

---

## Basic Config

`/etc/nginx/sites-available/default`

```nginx
server {
    listen 80;
    server_name example.com www.example.com;

    root /var/www/html;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

Enable it:

```bash
sudo ln -s /etc/nginx/sites-available/mysite /etc/nginx/sites-enabled/
sudo nginx -t          # test config
sudo systemctl reload nginx
```

---

## Serving Static Files

```nginx
server {
    listen 80;
    server_name static.example.com;

    root /var/www/static;

    location / {
        try_files $uri $uri/ =404;
    }

    # Cache static assets
    location ~* \.(css|js|png|jpg|jpeg|gif|ico|svg|woff2)$ {
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
```

---

## Reverse Proxy

Forward requests to a backend application:

```nginx
server {
    listen 80;
    server_name app.example.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### WebSocket Support

```nginx
location /ws {
    proxy_pass http://localhost:3000;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
}
```

---

## Load Balancing

```nginx
upstream backend {
    # Round-robin (default)
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
    server 127.0.0.1:8003;
}

# Or weighted
upstream backend_weighted {
    server 127.0.0.1:8001 weight=3;
    server 127.0.0.1:8002 weight=1;
}

# Or least connections
upstream backend_lc {
    least_conn;
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
}

server {
    listen 80;
    server_name lb.example.com;

    location / {
        proxy_pass http://backend;
    }
}
```

| Strategy | Directive | Behaviour |
|---|---|---|
| **Round Robin** | (default) | Rotate through servers equally |
| **Weighted** | `weight=N` | Higher weight = more requests |
| **Least Connections** | `least_conn` | Send to server with fewest active connections |
| **IP Hash** | `ip_hash` | Same client IP always hits same server |

---

## SSL/TLS (HTTPS)

### With Let's Encrypt (Certbot)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d example.com -d www.example.com
# Auto-configures nginx and sets up auto-renewal
```

### Manual SSL Config

```nginx
server {
    listen 443 ssl http2;
    server_name example.com;

    ssl_certificate     /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    location / {
        proxy_pass http://localhost:3000;
    }
}

# Redirect HTTP → HTTPS
server {
    listen 80;
    server_name example.com;
    return 301 https://$host$request_uri;
}
```

---

## Common Directives

| Directive | Purpose | Example |
|---|---|---|
| `listen` | Port & protocol | `listen 443 ssl http2;` |
| `server_name` | Domain matching | `server_name *.example.com;` |
| `root` | Document root | `root /var/www/html;` |
| `index` | Default file | `index index.html index.htm;` |
| `location` | URL path matching | `location /api { ... }` |
| `proxy_pass` | Reverse proxy target | `proxy_pass http://localhost:8080;` |
| `try_files` | File lookup fallback | `try_files $uri $uri/ /index.html;` |
| `return` | Redirect/response | `return 301 https://$host$request_uri;` |
| `rewrite` | URL rewriting | `rewrite ^/old(.*)$ /new$1 permanent;` |
| `client_max_body_size` | Max upload size | `client_max_body_size 50M;` |
| `gzip` | Compression | `gzip on;` |

---

## Useful Commands

```bash
sudo nginx -t                    # Test configuration syntax
sudo systemctl start nginx       # Start
sudo systemctl stop nginx        # Stop
sudo systemctl reload nginx      # Reload config (no downtime)
sudo systemctl restart nginx     # Full restart
sudo systemctl status nginx      # Check status

# Logs
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```
