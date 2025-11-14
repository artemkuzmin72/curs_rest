from datetime import timedelta

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit
from users.models import User


class HabitTestCase(APITestCase):
    def setUp(self):
        """Функция подготовки данных перед тестированием"""
        self.user = User.objects.create(email="admin@example.com")
        self.user.set_password("0147")
        self.client.force_authenticate(user=self.user)  # авторизуем пользователя
        self.habit = Habit.objects.create(
            owner=self.user,
            name="Ежедневная привычка",
            place="Дома",
            time="07:00:00",
            action="Делать упражнения",
            is_pleasant=False,
            periodicity=1,
            reward="Чашка кофе",
            execution_time=timedelta(seconds=60),
            is_published=True,
        )

    def test_habit_create(self):
        """Тестирование создания экземпляра привычки"""
        url = reverse("habit-list")
        data = {
            "name": "Новая привычка",
            "place": "В офисе",
            "time": "05:00:00",
            "action": "Читать книгу",
            "is_pleasant": False,
            "periodicity": 2,
            "execution_time": "00:01:00",  # 1 минута в формате HH:MM:SS
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.all().count(), 2)

    def test_habit_list(self):
        """Тестирование запроса на вывод списка привычек"""
        url = reverse("habit-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()["results"]), 1)

    def test_habit_retrieve(self):
        """Тестирование запроса на вывод полей привычки по заданному pk"""
        url = reverse("habit-detail", args=(self.habit.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("action"), self.habit.action)
        self.assertEqual(data.get("name"), self.habit.name)

    def test_habit_update(self):
        """Тестирование запроса на изменение полей привычки"""
        url = reverse("habit-detail", args=(self.habit.pk,))
        data_update = {
            "name": "Обновленная привычка",
            "place": "В спортзале",
            "action": "Плавание",
            "is_pleasant": False,
            "periodicity": 3,
            "reward": "Массаж",
            "time": "05:05:00",
            "execution_time": "00:01:05",
            "is_published": True,
        }
        response = self.client.patch(url, data=data_update)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("time"), "05:05:00")
        self.assertEqual(data.get("name"), "Обновленная привычка")

    def test_habit_delete(self):
        """Тестирование запроса на удаление привычки с заданным pk"""
        url = reverse("habit-detail", args=(self.habit.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.all().count(), 0)

    def test_habit_with_related_habit(self):
        """
        Тестирование создания привычки со связанной привычкой.
        Связанная привычка должна быть приятной.
        Основная привычка — НЕ приятная и без награды.
        """
        pleasant_habit = Habit.objects.create(
            name="Приятная привычка",
            owner=self.user,
            place="Дом",
            time="10:00",
            action="Пить чай",
            is_pleasant=True,
            periodicity=1,
            execution_time=timedelta(minutes=2),
            is_published=True,
        )

        data = {
            "name": "Основная привычка",
            "owner": self.user.id,
            "place": "Работа",
            "time": "12:00",
            "action": "Сделать зарядку",
            "is_pleasant": False,
            "related_habit": pleasant_habit.id,
            "periodicity": 1,
            "execution_time": "00:02:00",
            "is_published": True,
        }

        response = self.client.post("/api/habits/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
