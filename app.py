import time
import requests
from flask import Flask, jsonify
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

BOT_TOKEN = "8702482925:AAHxXWBrvDzFVpwW13r_O4Id0jyc0jUa2wM"
CHAT_ID = "-5124378185"

last_heartbeat_time = time.time()
is_power_on = True
TIMEOUT = 45

def send(msg):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": msg}
    )

#  شرط النبضات
def monitor():
    global is_power_on, last_heartbeat_time

    diff = time.time() - last_heartbeat_time

    #  انقطاع الكهرباء
    if is_power_on and diff > TIMEOUT:
        is_power_on = False
        send(" الكهرباء قطعت")

    #  رجوع الكهرباء
    elif not is_power_on and diff <= TIMEOUT:
        is_power_on = True
        send("الحمد لله الكهرباء جات")

scheduler = BackgroundScheduler()
scheduler.add_job(monitor, "interval", seconds=5)
scheduler.start()

@app.route("/heartbeat", methods=["POST"])
def heartbeat():
    global last_heartbeat_time
    last_heartbeat_time = time.time()
    return {"status": "ok"}

@app.route("/")
def home():
    return {"power": "ON" if is_power_on else "OFF"}
