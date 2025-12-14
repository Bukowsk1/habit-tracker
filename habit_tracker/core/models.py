from pydantic import BaseModel, Field, field_validator
from datetime import date

class Habit:
    """Внутренняя модель привычки для хранения в памяти."""
    def __init__(self, id: int, name: str, marks: list[date] | None = None) -> None:
        self.id: int = id
        self.name: str = name
        self.marks: list[date] = [] if marks is None else marks
        self.streak: int = 0


# Input
class HabitCreate(BaseModel):
    name: str = Field(...)
    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, v: str):
        if len(v.strip()) == 0:
            raise ValueError("Habit name cannot be empty.")
        return v.strip()


class HabitUpdate(HabitCreate):
    pass

#Output
class HabitBase(BaseModel):
    id: int = Field(...)
    name: str = Field(...)


class HabitResponse(HabitBase):
    marks: list[date] = Field(...)
    streak: int = Field(...)


class HabitMarkResponse(HabitBase):
    last_marked_at: date = Field(...)
    streak: int = Field(...)


class HabitStatsResponse(BaseModel):
    """Модель для ответа с статистикой привычки."""
    id: int
    name: str
    total_marks: int
    current_streak: int
    max_streak: int
    success_rate: float
    last_dates: list[date]

    class Config:
        json_encoders = {
            date: lambda v: v.isoformat()
        }
        