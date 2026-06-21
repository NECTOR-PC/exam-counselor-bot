import os
import telebot
from openai import OpenAI

# Environment Variables se keys le rahe hain (Security ke liye)
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
client = OpenAI(api_key=OPENAI_API_KEY)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "Hello Student! 🎓 Main ek Exam Counselor Bot hoon.\n\n"
        "Aap kisi bhi exam (jaise JEE, NEET, UPSC, SSC, Boards) ki details, pattern, "
        "eligibility, ya tips ke baare mein mujhse pooch sakte hain. Boliye, kis exam ki jankari chahiye?"
    )
    bot.reply_to(message, welcome_text)

@bot.message_handler(func=lambda message: True)
def answer_exam_query(message):
    bot.reply_to(message, "Jankari dhoondh raha hoon, kripya thoda intezaar karein... ⏳")
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system", 
                    "content": "Aap ek expert Indian Education Counselor hain. Students ko exams ke baare mein detailed aur accurate jankari dein. Apne jawab ko bullet points mein acche se format karein."
                },
                {
                    "role": "user", 
                    "content": message.text
                }
            ]
        )
        bot_reply = response.choices[0].message.content
        bot.send_message(message.chat.id, bot_reply, parse_mode="Markdown")
        
    except Exception as e:
        bot.reply_to(message, "Maaf kijiyega, server mein kuch problem aa gayi hai.")

bot.polling()
  
