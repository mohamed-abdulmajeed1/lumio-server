import time
import threading
import requests
from flask import Flask, jsonify

app = Flask(__name__)

BOT_TOKEN = "8702482925:AAHxXWBrvDzFVpwW13r_O4Id0jyc0jUa2wM"
CHAT_ID = "-5124378185"

last_heartbeat_time = time.time()
is_power_on = True
TIMEOUT = 45


def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": message
    }

    try:
        requests.post(url, data=data, timeout=10)
        print("Message sent:", message)

    except Exception as e:
        print("Telegram Error:", e)


#  داله  المراقبة 
def monitor_power():

    global last_heartbeat_time
    global is_power_on

    while True:

        diff = time.time() - last_heartbeat_time

        print("Checking...", int(diff), "seconds")

        # الكهرباء انقطعت
        if is_power_on and diff > TIMEOUT:

            is_power_on = False

            send_telegram_alert("الكهرباء قطعت ")

            print("Power OFF")

        # الكهرباء رجعت
        elif not is_power_on and diff <= TIMEOUT:

            is_power_on = True

            send_telegram_alert(" الحمد لله الكهرباء جات ")

            print("Power ON")

        time.sleep(5)


@app.route("/heartbeat", methods=["POST"])
def heartbeat():

    global last_heartbeat_time

    last_heartbeat_time = time.time()

    print("Heartbeat received")

    return jsonify({"status": "success"})


@app.route("/")
def home():

    diff = int(time.time() - last_heartbeat_time)

    return jsonify({
        "power": "ON" if is_power_on else "OFF",
        "last_seen": diff
    })


# backgraond mentoring
monitor_thread = threading.Thread(target=monitor_power)

monitor_thread.daemon = True

monitor_thread.start()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
