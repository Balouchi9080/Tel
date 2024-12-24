from flask import Flask, request
import telegram
import urllib.parse
from keep_alive import keep_alive

# توکن بات تلگرام
BOT_TOKEN = "7927361515:AAGhv5cQZz6K1aLxL-M6_sM6mqNYg8nzhxk"
bot = telegram.Bot(token=BOT_TOKEN)

# Flask اپلیکیشن برای وب‌هوک
app = Flask(__name__)

# ذخیره شماره‌گذاری لینک‌ها برای هر کاربر
user_counters = {}

@app.route('/webhook', methods=['POST'])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat.id
    text = update.message.text

    if text == "/start":
        bot.send_message(chat_id=chat_id, text="به بات تبدیل لینک خوش آمدید! لینک اولیه را ارسال کنید.")
    else:
        try:
            # چک کردن لینک و ایجاد لینک ثانویه
            user_id = str(chat_id)
            if user_id not in user_counters:
                user_counters[user_id] = 0
            user_counters[user_id] += 1
            link_number = user_counters[user_id]

            # ایجاد لینک ثانویه
            processed_link = f"https://example.com/processed?original={urllib.parse.quote(text)}&count={link_number}"
            bot.send_message(chat_id=chat_id, text=f"لینک شماره {link_number} شما:\n{processed_link}")
        except Exception as e:
            bot.send_message(chat_id=chat_id, text="مشکلی در پردازش لینک وجود دارد!")

    return "ok"

if __name__ == "__main__":
    keep_alive()
    app.run(host='0.0.0.0', port=8080)
