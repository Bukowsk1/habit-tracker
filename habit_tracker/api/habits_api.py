from fastapi import APIRouter, status, HTTPException
from habit_tracker.core.models import HabitResponse, HabitCreate, HabitMarkResponse, HabitBase, HabitUpdate
from habit_tracker.core import services

router = APIRouter()

@router.post("/", response_model=HabitBase, status_code=status.HTTP_201_CREATED)
def create_habit(habit: HabitCreate):
    """Создать новую привычку."""
    try:
        habit = services.create_habit(habit)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return habit


@router.get("/", response_model=list[HabitResponse])
def get_all_habits():
    """Получить список всех привычек."""
    all_habits = services.get_all_habits_with_details()
    return [
        HabitResponse(**habit)
        for habit in all_habits
    ]


@router.get("/{id}/", response_model=HabitResponse)
def get_habit(id: int):
    habit = services.get_habit_by_id_with_details(id)
    if habit is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Привычка с таким id не найдена.")
    return habit


@router.put("/{id}/", response_model=HabitBase, status_code=status.HTTP_200_OK)
def update_habit(id: int, habit_data: HabitUpdate):
    try:
        habit = services.update_habit(id, habit_data)
        if habit is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Привычка с таким id не найдена.")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return habit


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_habit(id: int):
    is_delete = services.delete_habit(id)
    if is_delete:
        return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Привычка с таким id не найдена.")


@router.post("/{id}/mark/", response_model=HabitMarkResponse, status_code=status.HTTP_200_OK)
def mark_habit(id: int):
    try:
        marked_habit = services.mark_habit(id)
        if marked_habit is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Привычка с таким id не найдена.")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return marked_habit





