import time
import requests
from flask import Flask, jsonify
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

BOT_TOKEN = "8702482925:AAHxXWBrvDzFVpwW13r_O4Id0jyc0jUa2wM"
CHAT_ID = "-5124378185"

last_heartbeat_time = time.time()
is_power_on = True
TIMEOUT_LIMIT = 45

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print("Error:", e)

# دالة الفحص التلقائي التي ستعمل في الخلفية
def auto_check_power():
    global last_heartbeat_time, is_power_on
    
    current_time = time.time()
    diff = current_time - last_heartbeat_time

    if is_power_on and diff > TIMEOUT_LIMIT:
        is_power_on = False
        send_telegram_alert("🚨 الكهرباء مقطوعة!")
        print("Alert Sent: Power OFF")

    elif not is_power_on and diff <= TIMEOUT_LIMIT:
        is_power_on = True
        send_telegram_alert("✅ الحمد لله الكهرباء رجعت")
        print("Alert Sent: Power ON")

# إعداد الـ Scheduler ليعمل كل 5 ثوانٍ ويفحص الحالة تلقائياً
scheduler = BackgroundScheduler()
scheduler.add_job(func=auto_check_power, trigger="interval", seconds=5)
scheduler.start()

@app.route("/heartbeat", methods=["POST"])
def heartbeat():
    global last_heartbeat_time
    last_heartbeat_time = time.time()
    return jsonify({"status": "success"})

@app.route("/")
def home():
    return f"Lumio Server - {'ON' if is_power_on else 'OFF'}"
