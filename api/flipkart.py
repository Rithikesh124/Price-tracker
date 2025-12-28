import os
from flask import Flask, request, render_template, jsonify
import telebot
from flipkart import get_product_details

# Fix for Vercel to find the templates folder correctly
template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
app = Flask(__name__, template_folder=template_dir)

# Get Token from Vercel Environment Variables
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
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "👋 Send me a Flipkart link!")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if "flipkart.com" in message.text:
        data = get_product_details(message.text)
        if "error" in data:
            bot.reply_to(message, "❌ Error fetching data")
        else:
            msg = f"📦 *{data['title']}*\n\n💰 Price: *{data['price']}*"
            if data['image']:
                bot.send_photo(message.chat.id, data['image'], caption=msg, parse_mode="Markdown")
            else:
                bot.send_message(message.chat.id, msg, parse_mode="Markdown")

# Crucial for Vercel: the app object must be available
# No need for if __name__ == "__main__":
