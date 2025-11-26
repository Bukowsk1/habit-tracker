from datetime import date
from typing import List
from pydantic import BaseModel, validator, Field


class Habit:
    def __init__(self, id: int, name: str, marks: List[date] = None):
        self.id: int = id
        self.name: str = name
        self.marks: List[date] = marks if marks is not None else []
        self.streak: int = 0

    def __repr__(self) -> str:
        return f"Habit(id={self.id!r}, name={self.name!r}, marks={self.marks!r})"


class HabitCreate(BaseModel):
    name: str = Field(...)

    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Habit name cannot be empty.')
        return v.strip()


class HabitResponse(BaseModel):
    id: int
    name: str


class HabitMarkResponse(BaseModel):
    id: int
    name: str
    last_marked_at: date
    streak: int


class HabitListResponse(BaseModel):
    id: int
    name: str
    marks: List[date] = []
    streak: int


class HabitUpdate(BaseModel):
    name: str = Field(...)

    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Habit name cannot be empty.')
        return v.strip()


class HabitBase(BaseModel):
    id: int
    name: str


class HabitResponse(HabitBase):
    marks: List[date] = []
    streak: int


class HabitDetailResponse(HabitBase):
    marks: List[date] = []
    streak: int
