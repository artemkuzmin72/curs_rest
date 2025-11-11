import requests

from config import settings


def send_telegram_message(chat_id, message):
    """Функция отправки уведомления в телеграмм"""
    params = {
        "text": message,
        "chat_id": chat_id,
    }
    requests.get(
        f"{settings.TELEGRAM_URL}{settings.TTELEGRAM_BOT_TOKEN}/sendMessage", params=params
    )
