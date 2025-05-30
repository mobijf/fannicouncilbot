from flask import Flask, request
import telebot
import os

TOKEN = os.environ.get("TOKEN", "7890945064:AAG0ocXX9wbarqPMP-I9jff6Vz0j7bipZTw")
CHAT_ID = os.environ.get("CHAT_ID", "8145564275")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return 'Bot is running!'

@app.route('/' + TOKEN, methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return 'ok', 200

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "سلام! می‌تونی پیامت رو بنویسی تا برسونیم به اعضای شورا.")

@bot.message_handler(func=lambda message: True)
def forward_message(message):
    try:
        user_info = bot.get_chat(message.chat.id)
        username = user_info.username if user_info.username else "کاربر ناشناس"
    except Exception:
        username = "کاربر ناشناس"

    bot.send_message(CHAT_ID, f"📩 پیام جدید از {username}:\n\n{message.text}")
    bot.reply_to(message, "پیامت به شورای صنفی فرستاده شد. مرسی از اعتمادت!")

# راه‌اندازی وبهوک (این باید فقط یک بار صدا زده بشه)
@app.before_first_request
def set_webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://YOUR-APP-NAME.vercel.app/' + TOKEN)