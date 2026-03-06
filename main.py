import os
import telebot
import requests
import google.generativeai as genai

TOKEN = os.getenv('TOKEN')
GEMINI_KEY = os.getenv('GEMINI_KEY')

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-pro')

bot = telebot.TeleBot(TOKEN)

PERSONALIDAD = """Eres un asistente simpático y divertido. 
Respondes de forma corta y casual, como si fueras un amigo."""

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "¡Hola! ¿En qué te puedo ayudar?")

@bot.message_handler(commands=['clima'])
def get_clima(message):
    try:
        ciudad = message.text.split(' ', 1)[1]
        url = f"https://wttr.in/{ciudad}?format=3&lang=es"
        respuesta = requests.get(url)
        bot.reply_to(message, respuesta.text)
    except IndexError:
        bot.reply_to(message, "Escribe la ciudad así: /clima Lima")

@bot.message_handler(func=lambda message: True)
def ai_response(message):
    try:
        respuesta = model.generate_content(PERSONALIDAD + "\nUsuario: " + message.text)
        bot.reply_to(message, respuesta.text)
    except Exception as e:
        bot.reply_to(message, "No pude responder, intenta de nuevo.")

bot.infinity_polling()