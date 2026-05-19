import time
import threading
import requests
from flask import Flask, jsonify

app = Flask(__name__)

# بيانات الاتصال بالبوت و القناة المسوله عن استلام الرسائل  
BOT_TOKEN = "8702482925:AAHxXWBrvDzFVpwW13r_O4Id0jyc0jUa2wM"
CHAT_ID = "-5124378185"

# إعدادات المتغيرات والوقت
last_heartbeat_time = time.time()
is_power_on = True
TIMEOUT_LIMIT = 45

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID, 
        "text": message
    }
    try:
        requests.post(url, data=data)
    except Exception as e:
        print("Error sending message:", e)

def monitor_power():
    global last_heartbeat_time, is_power_on
    while True:
        current_time = time.time()
        time_since_last_ping = current_time - last_heartbeat_time

        if is_power_on and time_since_last_ping > TIMEOUT_LIMIT:
            is_power_on = False
            send_telegram_alert("الكهرباء مقطوعه")

        elif not is_power_on and time_since_last_ping <= TIMEOUT_LIMIT:
            is_power_on = True
            send_telegram_alert("الحمد لله الكهرباء جات")

        time.sleep(10)

@app.route("/heartbeat", methods=["POST"])
def receive_heartbeat():
    global last_heartbeat_time
    last_heartbeat_time = time.time()
    return jsonify({"status": "success"}), 200

@app.route("/", methods=["GET"])
def home():
    status = "ON" if is_power_on else "OFF"
    return f"<h1>Lumio Server</h1><p>Status: {status}</p>"

if __name__ == "__main__":
    monitor_thread = threading.Thread(target=monitor_power, daemon=True)
    monitor_thread.start()
    app.run(host="0.0.0.0", port=5000)