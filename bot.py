import requests
import random
import os
from datetime import datetime
from flask import Flask

# 🌐 Flask server
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

# 🔐 Environment variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID") 
HF_TOKEN = os.getenv("HF_TOKEN")

# 📁 File to store daily count
DATA_FILE = "data.txt"

# 📊 Check daily limit
def can_send_today():
    today = str(datetime.now().date())

    try:
        with open(DATA_FILE, "r") as f:
            saved_date, count = f.read().split(",")
            count = int(count)
    except:
        saved_date = ""
        count = 0

    # Reset if new day
    if saved_date != today:
        count = 0

    if count < 5:
        return True, count, today
    return False, count, today

# 💾 Save count
def update_count(today, count):
    with open(DATA_FILE, "w") as f:
        f.write(f"{today},{count}")

# 🤖 AI generator
def generate_ai_message():
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "meta-llama/llama-3-8b-instruct",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a Tamil Gen Z friend texting casually in Tanglish. "
                    "Reply with ONLY one short sentence. "
                    "No explanations. No extra lines. "
                    "Sound like a real friend texting casually."
                )
            },
            {
                "role": "user",
                "content": "Send one random casual Tanglish message."
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        data = response.json()

        msg = data["choices"][0]["message"]["content"]
        msg = msg.strip().split("\n")[0]

        print("🤖 AI:", msg)
        return msg

    except Exception as e:
        print("❌ AI ERROR:", str(e))
        return "dei life la konjam try pannuda 😴"

# 📩 Telegram sender
def send_message(msg):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

        response = requests.post(url, data={
            "chat_id": CHAT_ID,
            "text": msg
        })

        print("📩 Telegram:", response.status_code)

    except Exception as e:
        print("❌ Telegram Error:", str(e))

# 🧪 MAIN ENDPOINT (triggered by uptime/cron)
@app.route('/ai-test')
def ai_test():
    print("🧪 Triggered")

    allowed, count, today = can_send_today()

    # 🎲 RANDOM LOGIC (adjust this value)
    if allowed and random.random() < 0.02:
        msg = generate_ai_message()
        send_message(msg)

        update_count(today, count + 1)

        return f"✅ Sent ({count+1}/5): {msg}"

    return f"⏭️ Skipped ({count}/5)"
    

# 🚀 Run server
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
