import os
from flask import Flask, request
import telebot

# Configuración — estas variables las defines en Render después
TOKEN = os.getenv('TOKEN')       # Tu API Token de BotFather
URL_APP = os.getenv('URL_APP')   # La URL que te dará Render (ej: https://mi-bot.onrender.com/)

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)


# ── Webhook endpoint: Telegram envía los mensajes aquí ──────────────────────
@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200


# ── Ruta raíz: registra (o re-registra) el webhook en Telegram ──────────────
@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=URL_APP + TOKEN)
    return "Bot funcionando correctamente ✅", 200


# ── Lógica del bot ───────────────────────────────────────────────────────────

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(
        message,
        "¡Hola! 👋 Soy tu bot funcional en Python.\n¿En qué puedo ayudarte?"
    )


@bot.message_handler(commands=['ayuda'])
def send_help(message):
    bot.reply_to(
        message,
        "Comandos disponibles:\n"
        "/start  — Saludo inicial\n"
        "/ayuda  — Esta lista de comandos"
    )


# Responde a cualquier otro mensaje de texto
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, f"Me dijiste: {message.text}")


# ── Arranque local (para pruebas) ────────────────────────────────────────────
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
