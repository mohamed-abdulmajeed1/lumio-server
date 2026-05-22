import time
import threading
import requests
from flask import Flask, jsonify

app = Flask(__name__)

# إعدادات البوت والتلغرام
BOT_TOKEN = "8702482925:AAHxXWBrvDzFVpwW13r_O4Id0jyc0jUa2wM"
CHAT_ID = "-5124378185"

# المتغيرات العامة (Global variables)
last_heartbeat_time = time.time()
TIMEOUT = 45
has_received_heartbeat = False  # الانتظار حتى أول نبضة لمنع الإنذار الكاذب عند الإقلاع

# جعلنا الحالة الافتراضية False حتى يرسل السيرفر تنبيه "الكهرباء رجعت" فور وصول أول نبضة
is_power_on = False  


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


# دالة المراقبة في الخلفية
def monitor_power():
    global is_power_on
    global last_heartbeat_time
    global has_received_heartbeat

    while True:
        # لا تفحص قبل أول heartbeat لمنع البلاغات الخاطئة
        if not has_received_heartbeat:
            print("Waiting for first heartbeat...")
            time.sleep(5)
            continue

        diff = time.time() - last_heartbeat_time
        print("Checking...", int(diff), "seconds")

        # الكهرباء انقطعت
        if is_power_on and diff > TIMEOUT:
            is_power_on = False
            send_telegram_alert("🚨 الكهرباء مقطوعة")
            print("Power OFF")

        # الكهرباء رجعت (ستتحقق هنا فور وصول أول نبضة بعد إقلاع السيرفر)
        elif not is_power_on and diff <= TIMEOUT:
            is_power_on = True
            send_telegram_alert("✅ الكهرباء رجعت")
            print("Power ON")

        time.sleep(5)


# الـ Route الخاص باستقبال نبضات القلب
@app.route("/heartbeat", methods=["POST"])
def heartbeat():
    global last_heartbeat_time
    global has_received_heartbeat

    last_heartbeat_time = time.time()
    has_received_heartbeat = True  # تفعيل الفحص وبدء المراقبة فوراً

    print("Heartbeat received")
    return jsonify({"status": "success"})


# الصفحة الرئيسية لعرض الحالة الحالية للمشروع
@app.route("/")
def home():
    diff = int(time.time() - last_heartbeat_time)
    return jsonify({
        "power": "ON" if is_power_on else "OFF",
        "has_started_monitoring": has_received_heartbeat,
        "last_seen_seconds_ago": diff if has_received_heartbeat else "No heartbeat yet"
    })


# تشغيل دالة المراقبة في Thread منفصل في الخلفية
monitor_thread = threading.Thread(target=monitor_power)
monitor_thread.daemon = True
monitor_thread.start()


if __name__ == "__main__":
    # تشغيل السيرفر ليقبل الاتصالات الخارجية عبر منفذ 5000
    app.run(host="0.0.0.0", port=5000)
