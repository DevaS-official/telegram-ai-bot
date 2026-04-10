import requests
import time
import random
import os
from datetime import datetime
from flask import Flask
from threading import Thread

# 🌐 Flask server
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

# 🧪 AI TEST ENDPOINT (IMPORTANT)
@app.route('/ai-test')
def ai_test():
    print("🧪 AI TEST TRIGGERED")

    msg = generate_ai_message()

    return f"""
    <h2>AI RESULT</h2>
    <p>{msg}</p>
    """

# 🔧 Dynamic port for Railway
def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# 🔐 Environment variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
HF_TOKEN = os.getenv("HF_TOKEN")

# 🤖 AI generator (FIXED + STRONG DEBUG)
def generate_ai_message():
    url = "https://router.huggingface.co/hf-inference/models/google/flan-t5-small"

    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "inputs": "Give a short, powerful motivational message (max 2 lines).",
        "parameters": {
            "max_new_tokens": 50
        }
    }

    try:
        print("🤖 Calling Hugging Face...")

        response = requests.post(url, headers=headers, json=payload)

        print("STATUS:", response.status_code)
        print("RAW RESPONSE:", response.text)

        data = response.json()

        # ✅ Correct parsing
        if isinstance(data, list) and "generated_text" in data[0]:
            return data[0]["generated_text"]

        else:
            print("⚠️ Unexpected response format:", data)
            return "⚠️ AI format error (check logs)"

    except Exception as e:
        print("❌ AI ERROR:", str(e))
        return "❌ AI failed (check Railway logs)"

# 📩 Telegram sender
def send_message(msg):
    try:
        print("📩 Sending Telegram message...")

        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        response = requests.post(url, data={
            "chat_id": CHAT_ID,
            "text": msg
        })

        print("Telegram STATUS:", response.status_code)
        print("Telegram RESPONSE:", response.text)

    except Exception as e:
        print("❌ Telegram Error:", str(e))

# 🚀 Start server
keep_alive()

print("🚀 Bot started...")

# 🔁 Bot logic
messages_sent_today = 0
current_day = datetime.now().day

send_message("🤖 Bot started successfully!")

while True:
    now = datetime.now()

    # 🔄 Reset daily count
    if now.day != current_day:
        messages_sent_today = 0
        current_day = now.day

    if messages_sent_today < 5:
        wait_time = random.randint(2, 5) * 60 * 60
        print(f"⏳ Waiting {wait_time/3600:.2f} hours...")

        time.sleep(wait_time)

        print("🧠 Generating AI message for auto send...")
        msg = generate_ai_message()

        send_message("🤖 AI says:\n\n" + msg)

        messages_sent_today += 1
        print(f"✅ Messages sent today: {messages_sent_today}")

    else:
        print("🛑 Daily limit reached. Sleeping 1 hour...")
        time.sleep(60 * 60)
