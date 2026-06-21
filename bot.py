import os
import telebot
from openai import OpenAI
from flask import Flask
import threading

# Keys le rahe hain (Render se aayengi)
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
client = OpenAI(api_key=OPENAI_API_KEY)

# --- DUMMY WEB SERVER (Render ke Port Error ko theek karne ke liye) ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running 24/7!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
# ---------------------------------------------------------

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "Hello Student! 🎓 Main ek Exam Counselor Bot hoon.\n\n"
        "Aap kisi bhi exam ki details, pattern, eligibility, ya tips ke baare mein mujhse pooch sakte hain."
    )
    bot.reply_to(message, welcome_text)

@bot.message_handler(func=lambda message: True)
def answer_exam_query(message):
    bot.reply_to(message, "Jankari dhoondh raha hoon, kripya thoda intezaar karein... ⏳")
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Aap ek expert Indian Education Counselor hain. Students ko exams ke baare mein detailed jankari dein."},
                {"role": "user", "content": message.text}
            ]
        )
        bot_reply = response.choices[0].message.content
        bot.send_message(message.chat.id, bot_reply, parse_mode="Markdown")
        
    except Exception as e:
        bot.reply_to(message, "Maaf kijiyega, server mein kuch problem aa gayi hai.")

# Dummy server aur Bot dono ko ek sath start karna
if __name__ == "__main__":
    threading.Thread(target=run_web).start()
    bot.polling(non_stop=True)
