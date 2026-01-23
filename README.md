# Habits REST API

REST API для управления привычками с интеграцией Telegram-уведомлений.

## Описание

Проект представляет собой Django REST API для создания и управления привычками пользователей. Система позволяет:

- Создавать, просматривать, редактировать и удалять привычки
- Настраивать напоминания через Telegram
- Публиковать привычки для общего доступа
- Связывать привычки между собой
- Автоматически отправлять напоминания через Celery

## Технологический стек

- **Django 5.2.7** - веб-фреймворк
- **Django REST Framework** - REST API
- **PostgreSQL** - база данных
- **Celery** - асинхронные задачи
- **Redis** - брокер сообщений для Celery
- **JWT** - аутентификация
- **Telegram Bot API** - отправка уведомлений
- **drf-yasg** - Swagger документация

## Структура проекта

```
curs_rest/
├── config/              # Настройки проекта
│   ├── settings.py     # Основные настройки
│   ├── urls.py         # Главный URL роутер
│   ├── celery.py       # Конфигурация Celery
│   └── ...
├── habits/             # Приложение привычек
│   ├── models.py       # Модель Habit
│   ├── views.py        # ViewSet для привычек
│   ├── serializers.py  # Сериализаторы
│   ├── tasks.py        # Celery задачи
│   ├── services.py     # Сервисы (Telegram)
│   └── ...
├── users/              # Приложение пользователей
│   ├── models.py       # Кастомная модель User
│   ├── views.py        # Регистрация
│   ├── serializers.py  # Сериализаторы
│   └── ...
└── requirements.txt    # Зависимости
```

## Установка и настройка

### Требования

- Python 3.13+
- PostgreSQL
- Redis
- Telegram Bot Token

### Установка

1. Клонируйте репозиторий:

```bash
git clone <repository-url>
cd curs_rest
```

2. Создайте виртуальное окружение:

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows
```

3. Установите зависимости:

```bash
pip install -r requirements.txt
```

4. Создайте файл `.env` в корне проекта:

```env
DATABASE_NAME=your_db_name
DATABASE_USER=your_db_user
DATABASE_PASSWORD=your_db_password
DATABASE_HOST=localhost
DATABASE_PORT=5432
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
STRIPE_SECRET_KEY=your_stripe_key  # опционально
```

5. Примените миграции:

```bash
python manage.py migrate
```

6. Создайте суперпользователя:

```bash
python manage.py createsuperuser
```

### Запуск

1. Запустите Redis (если не запущен):

```bash
redis-server
```

2. Запустите Celery worker:

```bash
celery -A config worker -l info
```

3. Запустите Celery beat (для периодических задач):

```bash
celery -A config beat -l info
```

4. Запустите Django сервер:

```bash
python manage.py runserver
```

## API Endpoints

### Аутентификация

- `POST /api/auth/register/` - Регистрация нового пользователя
- `POST /api/auth/login/` - Получение JWT токена
- `POST /api/auth/refresh/` - Обновление JWT токена

### Привычки

- `GET /api/habits/` - Список привычек (свои + публичные)
- `POST /api/habits/` - Создание новой привычки
- `GET /api/habits/{id}/` - Детали привычки
- `PUT /api/habits/{id}/` - Обновление привычки
- `PATCH /api/habits/{id}/` - Частичное обновление
- `DELETE /api/habits/{id}/` - Удаление привычки

### Документация

- `GET /swagger/` - Swagger UI
- `GET /redoc/` - ReDoc документация

## Модели данных

### User

Кастомная модель пользователя с email в качестве username:

- `email` - уникальный email
- `first_name`, `last_name` - имя и фамилия
- `city` - город
- `avatar` - аватар
- `chat_id` - ID чата в Telegram для уведомлений

### Habit

Модель привычки со следующими полями:

- `name` - название привычки
- `owner` - владелец (ForeignKey к User)
- `place` - место выполнения
- `time` - время выполнения
- `action` - действие
- `is_pleasant` - признак приятной привычки
- `related_habit` - связанная привычка (ForeignKey к Habit)
- `periodicity` - периодичность (раз в неделю, 1-7)
- `reward` - вознаграждение
- `execution_time` - время на выполнение (макс. 120 сек)
- `is_published` - признак публичности

### Валидация привычек

При сохранении выполняются следующие проверки:

- Нельзя одновременно указать `reward` и `related_habit`
- Время выполнения не может превышать 120 секунд
- Связанная привычка должна быть приятной (`is_pleasant=True`)
- У приятной привычки не может быть вознаграждения или связанной привычки
- Периодичность не может быть больше 7 дней

## Права доступа

- **Аутентифицированные пользователи** могут создавать привычки
- **Владелец** может редактировать и удалять свои привычки
- **Все пользователи** могут просматривать публичные привычки (`is_published=True`)
- **Только владелец** может просматривать свои приватные привычки

## Celery задачи

### Отправка напоминаний

Задача `send_habit_reminders` запускается каждую минуту через Celery Beat и отправляет напоминания пользователям в Telegram, если:

- У пользователя указан `chat_id`
- Время привычки совпадает с текущим временем

**Примечание**: В текущей реализации задачи используется поле `reminder_time`, которого нет в модели. Необходимо исправить на использование поля `time`.

## Переменные окружения

| Переменная           | Описание                    | Обязательная |
| -------------------- | --------------------------- | ------------ |
| `DATABASE_NAME`      | Имя базы данных PostgreSQL  | Да           |
| `DATABASE_USER`      | Пользователь БД             | Да           |
| `DATABASE_PASSWORD`  | Пароль БД                   | Да           |
| `DATABASE_HOST`      | Хост БД                     | Да           |
| `DATABASE_PORT`      | Порт БД (по умолчанию 5432) | Нет          |
| `TELEGRAM_BOT_TOKEN` | Токен Telegram бота         | Да           |
| `STRIPE_SECRET_KEY`  | Ключ Stripe (опционально)   | Нет          |

## Пагинация

По умолчанию используется пагинация с размером страницы 5 элементов. Для привычек используется кастомный пагинатор `HabitPagination`.

## CORS

Настроен CORS для работы с фронтендом. По умолчанию разрешены запросы с `http://localhost:8000`.

## Разработка

### Запуск тестов

```bash
python manage.py test
```

### Линтинг

```bash
flake8
```

## Лицензия

Проект создан в образовательных целях.
