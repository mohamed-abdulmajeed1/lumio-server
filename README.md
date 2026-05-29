```markdown
# Lumio (PowerPulse) — Power Outage Monitoring System

An automated, end-to-end engineering solution designed to monitor power stability and detect outages in real-time. This system utilizes a distributed architecture to ensure continuous tracking and immediate notification delivery whenever a power failure or network disruption occurs at the monitored site.

---

## System Architecture & Mechanism

The project is built on a client-server architecture driven by a continuous Heartbeat Mechanism:

1. Client-Side (Raspberry Pi): Deployed at the target location, a specialized Python script transmits periodic ping signals (Heartbeats) every 15 seconds to the remote server, indicating that both power and internet are stable.
2. Server-Side (Flask Backend): A lightweight backend hosted on Render receives these incoming signals and dynamically updates the system status.
3. Notification Layer (Telegram Bot API): If the server stops receiving heartbeats within a predefined threshold, it flags a power outage and instantly broadcasts an emergency alert to the user via the dedicated Telegram Bot.

> Engineering Advantage: The 15-second heartbeat interval serves an architectural double purpose. It keeps the Render free-tier instance active, effectively bypassing the 15-minute inactivity spin-down (sleep mode) as long as the target site has power.

---

## Key Features

* Real-Time Detection: Instantaneous tracking of power grid status without polling delays.
* Instantaneous Alerting: Critical failure alerts pushed directly to your devices via the @PLumioAlertBot Telegram channel.
* Isolated Environment Design: Fully compliant with modern Linux package management policies, ensuring host system stability.
* Resource Efficient: Minimal memory, CPU, and network bandwidth footprint on both the edge client and cloud server.

---

## Tech Stack

* Language: Python 3
* Backend Framework: Flask (Micro-framework)
* Environment Management: Python Virtual Environments (venv) / PEP 668 Compliant
* Protocols & Networking: HTTP POST Requests, cURL
* Cloud Infrastructure: Render Cloud Platform
* Version Control: Git & GitHub
* Notification Engine: Telegram Bot API

---

## Project Structure

```text
├── client/
│   └── client.py          # Script executing on the Raspberry Pi to send heartbeats
├── server/
│   └── server.py          # Flask backend handling state processing & alert triggers
├── requirements.txt       # Project dependencies and package listings
└── README.md              # Project documentation
```

---

## Installation & Setup

### 1. Environment Isolation (On Kali Linux / Raspberry Pi)
To prevent system-wide package conflicts (PEP 668 protection), initialize an isolated virtual environment:

```bash
# Create the project directory and navigate into it
mkdir ~/LumioProject && cd ~/LumioProject

# Initialize the virtual environment
python3 -m venv venv

# Activate the environment
source venv/bin/activate

# Install required network dependencies safely
pip install requests
```

### 2. Verifying the Telegram Bot API Pipeline
Run this quick cURL command from your terminal to verify that your bot credentials and chat routes are functioning correctly:

```bash
curl -X POST "[https://api.telegram.org/bot](https://api.telegram.org/bot)<YOUR_BOT_TOKEN>/sendMessage" \
     -d "chat_id=<YOUR_CHAT_ID>" \
     -d "text=Lumio System integrated successfully! The bot is armed and ready for alerts."
```

---

## Contributors & Credits
* Mohamed Abdelmajed — Software Engineer & Project Lead.
* Supervised by: Dr. Nishandra.
````</YOUR_CHAT_ID></YOUR_BOT_TOKEN>

```
