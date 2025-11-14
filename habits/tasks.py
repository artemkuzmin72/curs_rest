from celery import shared_task
from django.utils import timezone
from .models import Habit
from .services import send_telegram_message


@shared_task
def send_habit_reminders():
    now = timezone.now().time()
    habits = Habit.objects.filter(
        reminder_time__hour=now.hour, reminder_time__minute=now.minute
    )
    for habit in habits:
        user = habit.owner

        if not user or not user.chat_id:
            continue

        message = f"мне нужно {habit.action} в {habit.time} в {habit.place}"

        send_telegram_message(user.chat_id, message)
