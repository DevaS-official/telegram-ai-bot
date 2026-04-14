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
    send_message(msg)

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
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }

    # payload = {
    #     "model": "meta-llama/llama-3-8b-instruct",  # free model
    #     "messages": [
    #         #{"role": "user", "content": "Give a short motivational message (1-2 lines)."}
    #         {"role": "user", "content": "Give a short funny Tanglish message like Zomato notifications. Use Tamil + English mix, casual tone, only 1 line because i want to see it on notification, include humor about food, laziness, or daily life like a friend vibe only one msg is need not too many messages i want to see only 1 complete sentence dont give too many options. Make it Gen Z style."}
    #     ]
    # }

    payload = {
        "model": "meta-llama/llama-3-8b-instruct",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a Tamil Gen Z friend texting casually in Tanglish. "
                    "Reply with ONLY one short sentence. "
                    "No explanations. No quotes. No extra lines. "
                    "No prefixes like 'Here is your message'. "
                    "No emojis unless natural. "
                    "Sound like a real friend texting casually. "
                    "Topics can be anything: lazy, sleep, life, memes, random thoughts, fun, sarcasm. "
                    "Do NOT focus only on food."
                )
            },
            {
                "role": "user",
                "content": "Send one random casual Tanglish message."
            }
        ]
    }

    try:
        print("🤖 Calling OpenRouter AI...")

        response = requests.post(url, headers=headers, json=payload)

        print("STATUS:", response.status_code)
        print("RAW:", response.text)

        data = response.json()

        msg = data["choices"][0]["message"]["content"]
        msg = msg.strip().split("/n")[0]

        return msg

    except Exception as e:
        print("❌ AI ERROR:", str(e))
        return "⚡ Stay consistent. Keep pushing forward!"

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

        #send_message("🤖 AI says:\n\n" + msg)
        send_message(msg);

        messages_sent_today += 1
        print(f"✅ Messages sent today: {messages_sent_today}")

    else:
        print("🛑 Daily limit reached. Sleeping 1 hour...")
        time.sleep(60 * 60)
