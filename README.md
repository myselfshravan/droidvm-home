This is a folder in the "DroidVM" - an old Android 14 phone (vivo V2158) running Termux as a tiny home server.

SSH server on port `8022` | user: `u0_a315`

Python 3.12 installed

Can ssh -p 8022 u0_a315@192.168.1.45 to it if on the same network

or ssh -p 8022 u0_a315@100.94.102.37 if connected via Tailscale VPN with account "droidvmtailscale@gmail.com"

The Termux home folder is at /data/data/com.termux/files/home on the phone.

And this project folder is at /data/data/com.termux/files/home/droidvm-tools

I use tmux for long-running processes (FastAPI / scripts) and Tailscale for VPN to access the phone from other devices on different networks.
