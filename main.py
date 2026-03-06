import os
import telebot
import requests

TOKEN = os.getenv('TOKEN')
OPENROUTER_KEY = os.getenv('OPENROUTER_KEY')

bot = telebot.TeleBot(TOKEN)

PERSONALIDAD = """Eres un asistente simpático y divertido. 
Respondes de forma corta y casual, como si fueras un amigo."""

def preguntar_ia(texto):
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={"Authorization": f"Bearer {OPENROUTER_KEY}"},
        json={
            "model": "meta-llama/llama-3.2-3b-instruct:free",
            "messages": [
                {"role": "system", "content": PERSONALIDAD},
                {"role": "user", "content": texto}
            ]
        }
    )
    return response.json()['choices'][0]['message']['content']

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
        respuesta = preguntar_ia(message.text)
        bot.reply_to(message, respuesta)
    except Exception as e:
        bot.reply_to(message, f"Error: {e}")

bot.infinity_polling()