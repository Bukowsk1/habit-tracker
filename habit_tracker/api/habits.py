"""API роуты для управления привычками."""
from typing import List
from fastapi import APIRouter, status
from habit_tracker.core import services
from habit_tracker.core.models import (
    HabitCreate,
    HabitResponse,
    HabitMarkResponse,
    HabitListResponse,
)

router = APIRouter()


@router.post("/habits/", response_model=HabitResponse, status_code=status.HTTP_201_CREATED)
def create_habit(habit: HabitCreate):
    """Создать новую привычку."""
    created = services.create_habit(habit.name)
    return HabitResponse(id=created.id, name=created.name)


@router.post("/habits/{habit_id}/mark/", response_model=HabitMarkResponse)
def mark_habit(habit_id: int):
    """Отметить выполнение привычки за текущий день."""
    habit = services.mark_habit(habit_id)
    last = habit.marks[-1] if habit.marks else None
    return HabitMarkResponse(id=habit.id, name=habit.name, last_marked_at=last)


@router.get("/habits/", response_model=List[HabitListResponse])
def get_all_habits():
    """Получить список всех привычек."""
    habits = services.get_all_habits()
    result = []
    for h in habits:
        result.append(HabitListResponse(id=h.id, name=h.name, marks=h.marks))
    return result
