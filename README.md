Habit Tracker API
REST API для управления привычками (первая часть проекта)

Запуск проекта:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn habit_tracker.main:app --reload
```

Эндпоинты: 
- POST /habits/ - создать привычку
- POST /habits/{habit_id}/mark/ - отметить выполнение привычки на сегодня
- GET /habits/ - получить список привычек