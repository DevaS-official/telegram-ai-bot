import requests
import time
import random
import os
from datetime import datetime

# 🔐 Environment variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
HF_TOKEN = os.getenv("HF_TOKEN")

# 🤖 AI message generator (via Hugging Face)
def generate_ai_message():
    url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct"
    
    headers = {
        "Authorization": f"Bearer {HF_TOKEN}"
    }

    prompt = "Give a short, powerful motivational message (max 2 lines). No explanation."

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 60,
            "temperature": 0.9
        }
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        result = response.json()

        if isinstance(result, list) and "generated_text" in result[0]:
            text = result[0]["generated_text"]

            if prompt in text:
                text = text.replace(prompt, "").strip()

            return text
        else:
            print("Unexpected AI response:", result)
            return "⚡ Stay consistent. Your future depends on today."

    except Exception as e:
        print("AI Error:", e)
        return "🔥 Keep going. You’re stronger than your excuses."

# 📩 Send Telegram message
def send_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": message
    }

    try:
        response = requests.post(url, data=data)
        print("Telegram:", response.text)
    except Exception as e:
        print("Telegram Error:", e)

# 🔍 Check env variables
if not TELEGRAM_TOKEN or not CHAT_ID or not HF_TOKEN:
    print("❌ Missing environment variables!")
    exit()

# 🚀 Send startup message
print("Bot started...")
send_message("🤖 AI Bot is now running!")

# 📊 Daily control
messages_sent_today = 0
current_day = datetime.now().day

while True:
    now = datetime.now()

    # 🔄 Reset count if new day
    if now.day != current_day:
        messages_sent_today = 0
        current_day = now.day
        print("🔄 New day started. Counter reset.")

    # ✅ Only send if under limit
    if messages_sent_today < 5:
        wait_time = random.randint(2, 5) * 60 * 60  # 2–5 hours gap
        print(f"⏳ Waiting {wait_time/3600:.2f} hours...")
        time.sleep(wait_time)

        msg = generate_ai_message()
        send_message("🤖 AI says:\n\n" + msg)

        messages_sent_today += 1
        print(f"📨 Sent {messages_sent_today}/5 messages today")

    else:
        # 💤 Sleep until next day
        print("😴 Daily limit reached. Waiting for next day...")
        time.sleep(60 * 60)  # check every hour