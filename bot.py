import telebot
import time
import requests
import ssl

# Проверка наличия модуля SSL
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# Данные бота
BOT_TOKEN = "5373409081:AAEFe_FScq4B_xC56bJKAxUoDR6wuny5_KE"
CHANNEL_ID = "-1002271884534"  # ID канала
POST_LINK = "https://t.me/meditate_with_me/12"  # Ссылка на пост

# Запуск бота
bot = telebot.TeleBot(BOT_TOKEN, threaded=False)  # Отключаем многопоточность

def is_subscribed(user_id):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getChatMember?chat_id={CHANNEL_ID}&user_id={user_id}"
    response = requests.get(url).json()
    status = response.get("result", {}).get("status", "left")
    return status in ["member", "administrator", "creator"]

@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.chat.id
    if is_subscribed(user_id):
        bot.send_message(user_id, f"Вот ваша ссылка на пост: {POST_LINK}")
    else:
        bot.send_message(user_id, "❌ Вы не подписаны на канал! Подпишитесь: https://t.me/Inyeputi")

# Запуск бота без многопоточности
print("Бот запущен!")
try:
    bot.polling(none_stop=True, timeout=60)
except Exception as e:
    print(f"Ошибка: {e}")
