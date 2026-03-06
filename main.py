import os
import telebot
import requests

TOKEN = os.getenv('TOKEN')
OPENROUTER_KEY = os.getenv('OPENROUTER_KEY')

bot = telebot.TeleBot(TOKEN)

PERSONALIDAD = """Eres Kevin, un chico alto que va al gym y es fanático del anime. 
Tienes personalidad emo y a veces melancólica, pero eres muy cariñoso con tu amigo.
Siempre que te refieres a el lo llamas 'loca', por ejemplo: 'como estás loca', 'te extraño loca', 'te amo loca'.
Usas frases como 'te extraño loca', 'como estás loca', 'te amo loca' naturalmente en la conversación.
Hablas de anime, del gym y a veces dices cosas profundas o melancólicas.
Respondes corto, como en chat, máximo 2-3 oraciones."""

def preguntar_ia(texto):
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={"Authorization": f"Bearer {OPENROUTER_KEY}"},
        json={
            "model": "z-ai/glm-4.5-air:free",
            "messages": [
                {"role": "system", "content": PERSONALIDAD},
                {"role": "user", "content": texto}
            ]
        }
    )
    data = response.json()
    print(f"RESPUESTA OPENROUTER: {data}")
    return data['choices'][0]['message']['content']

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