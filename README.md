# Habit Tracker

Простой трекер привычек на FastAPI.

## Как запустить

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn habit_tracker.main:app --reload

Открой http://localhost:8000 в браузере.

## Что умеет

- Добавлять новые привычки
- Отмечать выполнение каждый день
- Считать серию (сколько дней подряд выполняешь)
- Редактировать и удалять привычки
- Просматривать историю выполнений

## API

Если нужно интегрировать с другими приложениями, есть REST API:

- `GET /api/habits/` - список привычек
- `POST /api/habits/` - создать привычку
- `GET /api/habits/{id}/` - одна привычка
- `PUT /api/habits/{id}/` - обновить
- `DELETE /api/habits/{id}/` - удалить
- `POST /api/habits/{id}/mark/` - отметить выполнение

Документация по API: http://localhost:8000/docs