# docs.droidvm.dev Website Specification

> A specification for an AI agent to build the documentation website for DroidVM.

---

## Overview

Build a modern, interactive documentation website for DroidVM that:
1. Explains what DroidVM is
2. Shows live stats from the actual phone
3. Provides setup guides
4. Will itself be hosted on DroidVM (inception!)

---

## Technical Requirements

### Framework
- **Preferred:** Astro, Next.js (static export), or plain HTML/CSS/JS
- **Must be:** Static or very lightweight (phone has limited resources)
- **Hosting:** Will run on port 8080 on the same phone, behind Cloudflare Tunnel

### Performance
- Fast load times (users might be on mobile)
- Minimal JavaScript
- Images optimized
- Dark mode support (important)

### Design
- Modern, clean, minimal
- Mobile-first (ironic if not)
- Code-friendly (monospace for commands)
- Copy buttons for code blocks

---

## Site Structure

```
docs.droidvm.dev/
├── /                    # Hero + overview
├── /quickstart          # 5-minute setup
├── /guide               # Full guide
│   ├── /setup          # Initial setup
│   ├── /tailscale      # Private access
│   ├── /cloudflare     # Public access
│   └── /tools          # DroidVM Tools API
├── /api                 # API documentation
├── /examples            # Use cases + code
├── /live                # Live stats from phone
└── /about               # Philosophy + credits
```

---

## Page Specifications

### 1. Home Page (`/`)

**Hero Section:**
```
╔═══════════════════════════════════════════════════╗
║                     DroidVM                       ║
║     Your Old Phone is a Cloud Server Now         ║
╚═══════════════════════════════════════════════════╝

That phone in your drawer? It's not e-waste.
It's an ARM Linux box waiting for a purpose.

[Get Started] [See Live Stats] [GitHub]
```

**Live Stats Widget:**
Pull from `https://api.droidvm.dev/status` every 30 seconds
```
┌─────────────────────────────────────┐
│ Live from an actual phone:         │
│                                     │
│ Platform: Linux (aarch64)          │
│ Memory: 4.42GB / 7.30GB            │
│ Processes: 20 running              │
│ Uptime: This website served from   │
│         the same phone you see here│
└─────────────────────────────────────┘
```

**What You Get:**
- SSH access from anywhere
- HTTPS APIs on custom domains
- System monitoring built-in
- No monthly fees
- No port forwarding
- Real cloud infrastructure

**Social Proof:**
- "Powered by a Vivo V2158"
- GitHub stars badge
- "X requests served today"

---

### 2. Quick Start (`/quickstart`)

**5-Minute Setup:**

Step-by-step with big, clear commands:

```bash
# Step 1: Install Termux
# (Link to F-Droid)

# Step 2: Run setup
pkg install curl -y
curl -sSL https://droidvm.dev/setup | bash

# Step 3: Follow wizard
# That's it!
```

**What Happens:**
Visual timeline of what the script does

**Result:**
Show expected output and access URLs

---

### 3. Full Guide (`/guide/*`)

**Tabbed or sidebar navigation:**
1. Initial Setup
2. SSH & tmux
3. Python Environment
4. Tailscale (Private Access)
5. Cloudflare Tunnel (Public Access)
6. DroidVM Tools API

Each section:
- Explanation of why
- Step-by-step commands
- Expected output
- Troubleshooting tips

---

### 4. API Documentation (`/api`)

**Interactive API Explorer:**

Show all endpoints with:
- Method (GET)
- Path (/status)
- Description
- Example response (formatted JSON)
- "Try it" button (hits real API)

**Endpoints to Document:**
```
GET /              → API info
GET /health        → Health check
GET /status        → Full system status
GET /system/info   → System information
GET /system/cpu    → CPU details
GET /system/memory → Memory usage
GET /system/disk   → Disk partitions
GET /system/battery → Battery (N/A on Termux)
GET /system/processes → Process count
GET /system/tmux   → tmux sessions
GET /network/info  → Network interfaces
GET /network/stats → Network I/O
GET /network/tailscale → Tailscale status
GET /network/ip    → IP addresses
```

---

### 5. Live Stats (`/live`)

**Real-time Dashboard:**

Fetch from `https://api.droidvm.dev/status` every 10 seconds

**Display:**
- System info (hostname, platform, Python version)
- Memory gauge (used vs total)
- CPU cores count
- Process list
- tmux sessions (show what's running)
- Last updated timestamp

**Meta:**
- "These stats come from: Vivo V2158"
- "Location: Drawer in Shravan's home"
- "Serving this website right now"

---

### 6. Examples (`/examples`)

**Use Cases:**

1. **Personal Status API**
   - Return "I'm busy" or "Available"
   - Integrate with calendar

2. **Webhook Handler**
   - Receive GitHub webhooks
   - Trigger home automation

3. **Feature Flags**
   - Simple JSON API for toggles
   - Update without deployments

4. **File Server**
   - Personal cloud storage
   - Upload/download files

5. **Home Automation Hub**
   - Control smart devices
   - Receive sensor data

Each example:
- Code snippet (Starlette/FastAPI)
- How to deploy
- Expected behavior

---

### 7. About (`/about`)

**The Story:**
Brief narrative of why DroidVM exists

**Philosophy:**
- Phones are computers
- E-waste problem
- DIY infrastructure
- Learning by building

**Credits:**
- Shravan (creator)
- Termux team
- Cloudflare
- Open source community

**Meta (the inception):**
"This entire website is hosted on the phone we're monitoring"

---

## Design System

### Colors
```css
/* Dark mode (default) */
--bg: #0f0f0f;
--text: #e0e0e0;
--accent: #00ff88;  /* Matrix green */
--code-bg: #1a1a1a;
--border: #333333;

/* Light mode */
--bg: #ffffff;
--text: #1a1a1a;
--accent: #00aa55;
--code-bg: #f5f5f5;
--border: #e0e0e0;
```

### Typography
```css
--font-main: 'Inter', sans-serif;
--font-mono: 'JetBrains Mono', monospace;
--font-size-base: 16px;
--line-height: 1.6;
```

### Components

**Code Block:**
```
┌─────────────────────────────┐
│ $ command here        [📋] │
│ output here                 │
└─────────────────────────────┘
```
- Syntax highlighting
- Copy button
- Line numbers (optional)

**Info Box:**
```
ℹ️ Note: Important information here
```

**Warning Box:**
```
⚠️ Warning: Be careful about this
```

**Live Data Badge:**
```
🟢 Live from DroidVM
```

---

## Interactive Elements

### 1. Live API Tester
```
Endpoint: [/status          ▾]
[Send Request]

Response:
{
  "success": true,
  "data": { ... }
}
```

### 2. Copy Command Buttons
Every code block has a one-click copy

### 3. Theme Toggle
Dark/Light mode switch (persist preference)

### 4. Status Indicator
Small badge showing if api.droidvm.dev is reachable

---

## SEO & Meta

```html
<title>DroidVM - Turn Your Old Android Phone Into a Cloud Server</title>
<meta name="description" content="Transform any old Android phone into a cloud-accessible server with SSH, HTTPS APIs, and custom domains. No root required.">
<meta property="og:image" content="https://docs.droidvm.dev/social-card.png">
```

**Keywords:**
- Old phone server
- Android home server
- Termux server
- DIY cloud
- Phone as VM
- Self-hosted
- E-waste reuse

---

## Footer

```
────────────────────────────────────────────
DroidVM - Old phones deserve a second life

GitHub | Twitter | Discord

🔴 This website is hosted on a phone
   See live stats: api.droidvm.dev/status

© 2025 Shravan | MIT License
────────────────────────────────────────────
```

---

## Technical Implementation

### For Static Generation (Recommended)
```bash
# Build static site
npm run build

# Output to ~/droidvm-docs/dist
# Then serve via Uvicorn static files or nginx
```

### Serving from Phone
```python
# Simple static file server
from starlette.applications import Starlette
from starlette.staticfiles import StaticFiles

app = Starlette()
app.mount("/", StaticFiles(directory="dist", html=True))
```

### Cloudflare Config
Add to `config.yml`:
```yaml
ingress:
  - hostname: docs.droidvm.dev
    service: http://localhost:8080
```

---

## Content Tone

**Voice:**
- Technical but friendly
- Honest about limitations
- Excited but not overhyped
- Educational focus
- Self-aware humor

**Example:**
```
"Yes, this is slightly ridiculous. Yes, it actually works.
And yes, we're kind of proud of it."
```

---

## Deployment

1. AI generates static site
2. Build outputs to `/dist`
3. Commit to `droidvm-docs` repo
4. Clone on phone
5. Serve via Python (Starlette/FastAPI static files)
6. Add `docs.droidvm.dev` to Cloudflare Tunnel config
7. The website about DroidVM is now hosted on DroidVM

**The inception is complete.**

---

## Success Metrics

- Load time < 2 seconds
- Works on mobile perfectly
- Live stats actually live
- Copy buttons work
- Dark mode looks good
- People can follow quickstart successfully
- GitHub stars increase
- Social shares

---

## References

- Read `DROIDVM_CONTEXT.md` for all technical details
- Read `OPEN_SOURCE_PLAN.md` for setup tool structure
- Read `context_cloudflare.md` for tunnel setup story
- Read `context_ngrok.md` for evolution narrative

---

Build this website. Make it beautiful. Make it fast. Make it honest about what this is: a beautiful hack that turns old phones into legitimate infrastructure.

And then host it on the same phone. Because why not.
