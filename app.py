import time
import requests
from flask import Flask, jsonify

app = Flask(__name__)

# إعدادات البوت والتلغرام
BOT_TOKEN = "8702482925:AAHxXWBrvDzFVpwW13r_O4Id0jyc0jUa2wM"
CHAT_ID = "-5124378185"

# المتغيرات العامة
last_heartbeat_time = None  # نبدأ بـ None لمعرفة هل استلمنا أي شيء أم لا
is_power_on = False  
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


# دالة ذكية لتحديث الحالة يتم استدعاؤها عند أي طلب دون الحاجة لـ Thread
def update_power_status():
    global is_power_on, last_heartbeat_time
    
    if last_heartbeat_time is None:
        return  # لم تصل أي نبضة بعد منذ إقلاع السيرفر الحالي

    diff = time.time() - last_heartbeat_time

    # الكهرباء انقطعت
    if is_power_on and diff > TIMEOUT:
        is_power_on = False
        send_telegram_alert("🚨 الكهرباء مقطوعة")
        print("Power OFF status updated")

    # الكهرباء رجعت
    elif not is_power_on and diff <= TIMEOUT:
        is_power_on = True
        send_telegram_alert("✅ الكهرباء رجعت")
        print("Power ON status updated")


@app.route("/heartbeat", methods=["POST"])
def heartbeat():
    global last_heartbeat_time
    
    last_heartbeat_time = time.time()
    
    # تحديث الحالة فوراً عند استقبال النبضة لمعرفة هل رجعت الكهرباء أم لا
    update_power_status()

    print("Heartbeat received")
    return jsonify({"status": "success"})


@app.route("/")
def home():
    global is_power_on
    
    # تحديث الحالة فوراً عند طلب الصفحة لرؤية الحالة الحقيقية
    update_power_status()

    if last_heartbeat_time is None:
        return jsonify({
            "power": "UNKNOWN",
            "has_started_monitoring": False,
            "last_seen_seconds_ago": "No heartbeat yet"
        })

    diff = int(time.time() - last_heartbeat_time)
    
    # تأكيد إضافي في حال انتهى وقت المهلة أثناء طلب الصفحة
    current_power = "ON" if (diff <= TIMEOUT and is_power_on) else "OFF"

    return jsonify({
        "power": current_power,
        "has_started_monitoring": True,
        "last_seen_seconds_ago": diff
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
