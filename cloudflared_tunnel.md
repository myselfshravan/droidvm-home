# **1. Environment**

- I am running **Termux** on Android, using **proot-distro** with an Ubuntu environment.
- I am using **tmux** to keep sessions running persistently.

Current tmux sessions:

```
cloudflared       → running the Cloudflare Tunnel
droidvm-tools     → running your API on localhost:8000
main             → running an example app on localhost:8090
```

---

# **2. Cloudflare Tunnel Setup (working parts)**

### **Step 1 — Install cloudflared**

Downloaded binary and set it up:

```bash
# Download cloudflared
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -O cloudflared

# Make it executable
chmod +x cloudflared

# Move to a location in PATH
mv cloudflared /usr/local/bin/

# Verify version
cloudflared --version
```

---

### **Step 2 — Authenticate cloudflared with Cloudflare**

```bash
cloudflared tunnel login
```

- Open the URL in your browser.
- Cloudflare generated `cert.pem` at `/root/.cloudflared/cert.pem`.

---

### **Step 3 — Create a tunnel**

```bash
cloudflared tunnel create shravan-tunnel
```

- Created tunnel with ID: `fab47e5c-2ab4-41db-a985-082630e66969`
- Credentials stored in `/root/.cloudflared/fab47e5c-2ab4-41db-a985-082630e66969.json`.

---

### **Step 4 — Configure tunnel to forward multiple services**

File: `/root/.cloudflared/config.yml`

```yaml
tunnel: fab47e5c-2ab4-41db-a985-082630e66969
credentials-file: /root/.cloudflared/fab47e5c-2ab4-41db-a985-082630e66969.json

ingress:
  - hostname: api.droidvm.dev
    service: http://localhost:8000
  - hostname: app.droidvm.dev
    service: http://localhost:8090
  - service: http_status:404
```

- **api.droidvm.dev** → forwards to `localhost:8000` (your API)
- **app.droidvm.dev** → forwards to `localhost:8090` (example app)

---

### **Step 5 — Create DNS routes in Cloudflare**

```bash
cloudflared tunnel route dns shravan-tunnel api.droidvm.dev
cloudflared tunnel route dns shravan-tunnel app.droidvm.dev
```

- Automatically created the CNAME records in Cloudflare.

---

### **Step 6 — Run the tunnel in tmux**

```bash
tmux new -s cloudflared
cloudflared tunnel run shravan-tunnel
# Detach tmux: Ctrl+b then d
```

- Tunnel runs persistently in background.
- Accessible via HTTPS:

  - `https://api.droidvm.dev` → localhost:8000
  - `https://app.droidvm.dev` → localhost:8090

---

# **3. Local services**

### **DroidVM Tools API**

- Running in tmux session `droidvm-tools`:

```bash
# Example to run Uvicorn server
uvicorn main:app --host 0.0.0.0 --port 8000
```

- Confirmed working:

```bash
curl -I http://localhost:8000
# HTTP/1.1 405 Method Not Allowed (expected for HEAD request)
curl http://localhost:8000
# {"name":"DroidVM Tools API","version":"0.1.0","status":"running", ...}
```

- Cloudflare Tunnel forwards `https://api.droidvm.dev` to this API.

---

### **Optional app on port 8090**

- Running any HTTP service (example: Uvicorn, Flask, or Python HTTP server).
- Confirmed working:

```bash
curl -I http://localhost:8090
# HTTP/1.1 200 OK
```

- Cloudflare Tunnel forwards `https://app.droidvm.dev` to this app.

---

# **4. Notes / gotchas**

1. **No need for ngrok anymore** — Cloudflare Tunnel supports multiple services/subdomains on the same tunnel.
2. **Ports are local** — Tunnel only works if your services are actually running locally.
3. **Permissions in Termux/proot-distro** — Commands like `ss -tulpn` may fail; use `curl` to check services instead.
4. **HTTPS automatically handled** by Cloudflare; no need for local SSL.
5. **Multiple subdomains** can be added via `config.yml` + `cloudflared tunnel route dns`.

---

# ✅ **Summary of URLs**

| Subdomain                                          | Local port | Service             |
| -------------------------------------------------- | ---------- | ------------------- |
| [https://api.droidvm.dev](https://api.droidvm.dev) | 8000       | DroidVM Tools API   |
| [https://app.droidvm.dev](https://app.droidvm.dev) | 8090       | Example app/service |

---

# **5. Persistent setup**

- Both your services and Cloudflare Tunnel are running in **tmux**, so you can detach and they stay alive.
- For fully hands-off startup, you could later set up scripts to start tmux sessions automatically when Termux starts.

---

This is the **complete working setup**.
