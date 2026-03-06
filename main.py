import os
import logging
from flask import Flask, request
import telebot

logging.basicConfig(level=logging.DEBUG)

TOKEN = os.getenv('TOKEN')
URL_APP = os.getenv('URL_APP')

print(f"TOKEN cargado: {TOKEN is not None}")
print(f"URL_APP cargado: {URL_APP}")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    try:
        json_string = request.get_data().decode('utf-8')
        print(f"Mensaje recibido COMPLETO: {json_string}")
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        print("Mensaje procesado OK")
    except Exception as e:
        print(f"ERROR DETALLADO: {e}")
        import traceback
        traceback.print_exc()
    return "!", 200

@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=URL_APP + TOKEN)
    return "Bot funcionando correctamente ✅", 200

@bot.message_handler(commands=['start'])
def send_welcome(message):
    print("Ejecutando /start")
    bot.reply_to(message, "¡Hola! 👋 Soy tu bot funcional en Python.\n¿En qué puedo ayudarte?")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    print(f"Mensaje de texto: {message.text}")
    bot.reply_to(message, f"Me dijiste: {message.text}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))