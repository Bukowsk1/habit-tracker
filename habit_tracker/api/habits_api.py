from fastapi import APIRouter, status
from habit_tracker.core.models import HabitResponse, HabitCreate, HabitMarkResponse, HabitBase, HabitUpdate, HabitStatsResponse
from habit_tracker.core import services

router = APIRouter()

@router.post("/", response_model=HabitBase, status_code=status.HTTP_201_CREATED)
def create_habit_endpoint(habit: HabitCreate):
    """Создать новую привычку."""
    return services.create_habit(habit)


@router.get("/", response_model=list[HabitResponse])
def get_all_habits():
    """Получить список всех привычек."""
    habits = get_all_habits()
    return [
        HabitResponse(
            id=habit.id,
            name=habit.name,
            marks=habit.marks,
            streak=services.calculate_streak(habit.marks)
        )
        for habit in habits
    ]


@router.get("/{habit_id}/", response_model=HabitResponse)
def get_habit(habit_id: int):
    habit = services.get_habit_by_id(habit_id)
    return HabitResponse(
        id=habit.id,
        name=habit.name,
        marks=habit.marks,
        streak=services.calculate_streak(habit.marks)
    )


@router.put("/{habit_id}/", response_model=HabitBase, status_code=status.HTTP_200_OK)
def update_habit_endpoint(habit_id: int, habit_data: HabitUpdate):
    habit = services.update_habit(habit_id, habit_data)
    return HabitBase(id=habit.id, name=habit.name)


@router.delete("/{habit_id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_habit_endpoint(habit_id: int):
    services.delete_habit(habit_id)


@router.post("/{habit_id}/mark/", response_model=HabitMarkResponse, status_code=status.HTTP_200_OK)
def mark_habit(habit_id: int):
    habit = services.mark_habit_completed(habit_id)
    return HabitMarkResponse(
        id=habit.id,
        name=habit.name,
        last_marked_at=services.TODAY,
        streak=services.calculate_streak(habit.marks)
    )


@router.get("/{habit_id}/stats/", response_model=HabitStatsResponse)
def get_habit_stats(habit_id: int):
    """Получить статистику по привычке."""
    habit = services.get_habit_by_id(habit_id)
    stats = services.calculate_habit_stats(habit)
    return HabitStatsResponse(
        id=habit.id,
        name=habit.name,
        **stats
    )





