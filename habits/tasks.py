from celery import shared_task
from django.utils import timezone
from .models import Habit
from .services import send_telegram_message


@shared_task
def send_habit_reminders():
    now = timezone.now().time()
    habits = Habit.objects.filter(reminder_time__hour=now.hour,
                                  reminder_time__minute=now.minute)
    for habit in habits:
        if habit.owner.profile.telegram_chat_id:  # Предполагаем, что у пользователя есть chat_id
            send_telegram_message(
                chat_id=habit.owner.profile.telegram_chat_id,
                text=f"Напоминание: пора выполнять привычку '{habit.name}'"
            )
