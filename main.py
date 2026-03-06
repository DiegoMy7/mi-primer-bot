import os
from flask import Flask, request
import telebot

TOKEN = os.getenv('TOKEN')
URL = os.getenv('URL_APP')

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=URL + TOKEN)
    return "Bot funcionando correctamente", 200

@bot.message_handler(commands=['start'])
def send_welcome(message):
    print("EJECUTANDO START")
    try:
        bot.reply_to(message, "¡Hola! Soy tu bot funcional en Python.")
        print("RESPUESTA ENVIADA OK")
    except Exception as e:
        print(f"ERROR AL RESPONDER: {e}")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    print(f"MENSAJE: {message.text}")
    try:
        bot.reply_to(message, f"Me dijiste: {message.text}")
        print("RESPUESTA OK")
    except Exception as e:
        print(f"ERROR: {e}")