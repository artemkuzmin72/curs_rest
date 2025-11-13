from django.db import models
from datetime import timedelta
from rest_framework.exceptions import ValidationError
# Create your models here.


class Habit(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Владелец",
    )
    place = models.CharField(max_length=100, verbose_name="Место")
    time = models.TimeField(verbose_name="Время")
    action = models.CharField(max_length=100, verbose_name="Действие")
    is_pleasant = models.BooleanField(default=True, verbose_name="Признак приятной привычки")
    related_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Связанная привычка",
    )
    periodicity = models.PositiveIntegerField(default=1, verbose_name="Число повторений в неделю")
    reward = models.CharField(max_length=100, null=True, blank=True, verbose_name="Вознаграждение")
    execution_time = models.DurationField(default=timedelta(minutes=2), verbose_name="Время на выполнение")
    is_published = models.BooleanField(default=True, verbose_name="Признак публичности")

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"

    def clean(self):
        """
        Выполняет все проверки перед сохранением модели.
        """
        if self.reward and self.related_habit:
            raise ValidationError("Нельзя одновременно указать вознаграждение и связанную привычку.")

        if self.execution_time > timedelta(seconds=120):
            raise ValidationError("Время выполнения не может превышать 120 секунд.")

        if self.related_habit and not self.related_habit.is_pleasant:
            raise ValidationError("Связанная привычка должна быть приятной.")

        if self.is_pleasant and (self.reward or self.related_habit):
            raise ValidationError("У приятной привычки не может быть вознаграждения или связанной привычки.")

        if self.periodicity > 7:
            raise ValidationError("Нельзя выполнять привычку реже, чем 1 раз в 7 дней.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({'публичная' if self.is_published else 'личная'})"
