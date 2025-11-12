"""Модели данных для привычек."""
from datetime import date
from typing import List
from pydantic import BaseModel, validator, Field


class Habit:
    """Внутренняя модель привычки для хранения в памяти."""

    def __init__(self, id: int, name: str):
        """Инициализировать поля."""
        self.id: int = id
        self.name: str = name
        self.marks: List[date] = []

    def __repr__(self) -> str:
        return f"Habit(id={self.id!r}, name={self.name!r}, marks={self.marks!r})"


class HabitCreate(BaseModel):
    """Модель для создания привычки."""
    name: str = Field(...)

    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Habit name cannot be empty.')
        return v.strip()


class HabitResponse(BaseModel):
    """Модель ответа после создания привычки."""
    id: int
    name: str


class HabitMarkResponse(BaseModel):
    """Модель ответа после отметки."""
    id: int
    name: str
    last_marked_at: date


class HabitListResponse(BaseModel):
    """Модель для списка привычек."""
    id: int
    name: str
    marks: List[date] = []
