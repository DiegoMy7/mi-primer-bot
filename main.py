import os
import telebot
import requests

TOKEN = os.getenv('TOKEN')
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "¡Hola! Soy tu bot funcional en Python.\nUsa /clima <ciudad> para ver el clima.")

@bot.message_handler(commands=['clima'])
def get_clima(message):
    try:
        ciudad = message.text.split(' ', 1)[1]
        url = f"https://wttr.in/{ciudad}?format=3&lang=es"
        respuesta = requests.get(url)
        bot.reply_to(message, respuesta.text)
    except IndexError:
        bot.reply_to(message, "Escribe la ciudad así: /clima Lima")
    except Exception as e:
        bot.reply_to(message, "No pude obtener el clima, intenta de nuevo.")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, f"Me dijiste: {message.text}")

bot.infinity_polling()