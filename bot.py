import requests
import time
import random
import os
from datetime import datetime
from flask import Flask
from threading import Thread

# 🌐 Keep-alive server
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# 🔐 Environment variables (set in Replit Secrets)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
HF_TOKEN = os.getenv("HF_TOKEN")

# 🤖 AI generator
def generate_ai_message():
    url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct"
    
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}

    payload = {
        "inputs": "Give a short, powerful motivational message (max 2 lines).",
        "parameters": {"max_new_tokens": 60, "temperature": 0.9}
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        result = response.json()

        print("🤖 Generating AI message...")
        print("STATUS:", response.status_code)
        print("RESPONSE:", response.text)

        if isinstance(result, list):
            return result[0]["generated_text"]
        return "⚡ Stay consistent. Keep pushing forward!"

    except:
        return "🔥 Keep going. You’re stronger than you think!"

# 📩 Telegram sender
def send_message(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

# 🚀 Start server
keep_alive()

# 🔁 Bot logic
messages_sent_today = 0
current_day = datetime.now().day

send_message("🤖 Bot started successfully!")

while True:
    now = datetime.now()

    if now.day != current_day:
        messages_sent_today = 0
        current_day = now.day

    if messages_sent_today < 5:
        time.sleep(random.randint(2, 5) * 60 * 60)

        msg = generate_ai_message()
        send_message("🤖 AI says:\n\n" + msg)

        messages_sent_today += 1
    else:
        time.sleep(60 * 60)
