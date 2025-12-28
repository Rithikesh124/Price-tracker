import os
import sys

# THIS IS THE FIX: Add the current directory to the system path
sys.path.append(os.path.dirname(__file__))

from flask import Flask, request, render_template, jsonify
import telebot
from flipkart import get_product_details  # Now it will find it!

# Fix for Vercel to find the templates folder correctly
template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
app = Flask(__name__, template_folder=template_dir)

# ... (rest of your code below)
BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN, threaded=False)

@app.route('/')
def home():
    url = request.args.get('url')
    if url:
        data = get_product_details(url)
        if "error" in data:
            return jsonify(data), 400
        return render_template('index.html', product=data)
    return render_template('index.html', product=None)

@app.route(f'/{BOT_TOKEN}', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        return jsonify({"status": "forbidden"}), 403

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "👋 Send me a Flipkart link!")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if "flipkart.com" in message.text or "fkrt.it" in message.text:
        data = get_product_details(message.text)
        if "error" in data:
            bot.reply_to(message, "❌ Error fetching data")
        else:
            msg = f"📦 *{data['title']}*\n\n💰 Price: *{data['price']}*\n⭐ Rating: {data['rating']}"
            if data['image']:
                bot.send_photo(message.chat.id, data['image'], caption=msg, parse_mode="Markdown")
            else:
                bot.send_message(message.chat.id, msg, parse_mode="Markdown")
