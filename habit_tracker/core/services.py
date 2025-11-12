"""Бизнес-логика для работы с привычками."""
from datetime import date
from typing import Dict, List
from fastapi import HTTPException
from habit_tracker.core.models import Habit

habits_db: Dict[int, Habit] = {}
_next_id = 1


def create_habit(name: str) -> Habit:
    """Создать новую привычку."""
    global _next_id
    if not name or not name.strip():
        raise HTTPException(status_code=400, detail="Habit name cannot be empty.")

    for h in habits_db.values():
        if h.name == name:
            raise HTTPException(status_code=400, detail="Habit with this name already exists.")

    habit = Habit(id=_next_id, name=name)
    habits_db[_next_id] = habit
    _next_id += 1
    return habit


def mark_habit(habit_id: int) -> Habit:
    """Отметить выполнение привычки за текущий день."""
    habit = habits_db.get(habit_id)
    if habit is None:
        raise HTTPException(status_code=404, detail="Habit not found.")

    today = date.today()
    if today in habit.marks:
        raise HTTPException(status_code=400, detail="Habit already marked for today.")

    habit.marks.append(today)
    return habit


def get_all_habits() -> List[Habit]:
    """Получить список всех привычек."""
    return list(habits_db.values())
