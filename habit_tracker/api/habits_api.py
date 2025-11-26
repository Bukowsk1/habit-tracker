from typing import List
from fastapi import APIRouter, status, HTTPException
from habit_tracker.core.services import (
    create_habit,
    get_all_habits_with_details,
    get_habit_by_id_with_details,
    update_habit,
    delete_habit,
    mark_habit,
)
from habit_tracker.core.models import (
    HabitCreate,
    HabitUpdate,
    HabitBase,
    HabitResponse,
    HabitMarkResponse,
)

router = APIRouter()


@router.post("/habits/", response_model=HabitResponse, status_code=status.HTTP_201_CREATED)
def create_habit_endpoint(habit: HabitCreate):
    try:
        created = create_habit(habit)
        return HabitResponse(id=created.id, name=created.name, marks=created.marks, streak=created.streak)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/habits/", response_model=List[HabitResponse])
def get_all_habits_endpoint():
    habits = get_all_habits_with_details()
    result = []
    for h in habits:
        result.append(HabitResponse(
            id=h['id'],
            name=h['name'],
            marks=h['marks'],
            streak=h['streak']
        ))
    return result


@router.get("/habits/{habit_id}/", response_model=HabitResponse)
def get_habit_by_id_endpoint(habit_id: int):
    habit = get_habit_by_id_with_details(habit_id)
    if habit is None:
        raise HTTPException(status_code=404, detail="Habit not found")
    return HabitResponse(
        id=habit['id'],
        name=habit['name'],
        marks=habit['marks'],
        streak=habit['streak']
    )


@router.put("/habits/{habit_id}/", response_model=HabitResponse)
def update_habit_endpoint(habit_id: int, habit: HabitUpdate):
    try:
        updated = update_habit(habit_id, habit)
        if updated is None:
            raise HTTPException(status_code=404, detail="Habit not found")
        return HabitResponse(id=updated.id, name=updated.name, marks=updated.marks, streak=updated.streak)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/habits/{habit_id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_habit_endpoint(habit_id: int):
    if not delete_habit(habit_id):
        raise HTTPException(status_code=404, detail="Habit not found")


@router.post("/habits/{habit_id}/mark/", response_model=HabitMarkResponse)
def mark_habit_endpoint(habit_id: int):
    try:
        result = mark_habit(habit_id)
        if result is None:
            raise HTTPException(status_code=404, detail="Habit not found")
        return HabitMarkResponse(
            id=result['id'],
            name=result['name'],
            last_marked_at=result['last_marked_at'],
            streak=result['streak']
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
