from datetime import date, timedelta
from typing import Dict, List
from habit_tracker.core.models import Habit

TODAY = date(2025, 7, 12)

habits_db: Dict[int, Habit] = {
    1: Habit(id=1, name="Бег", marks=[date(2025, 7, 10), date(2025, 7, 11)]),
    2: Habit(id=2, name="Чтение", marks=[date(2025, 7, 11)]),
    3: Habit(id=3, name="Медитация", marks=[])
}
next_habit_id = 4


def calculate_streak(marks: List[date]) -> int:
    if not marks:
        return 0

    sorted_marks = sorted(set(marks), reverse=True)

    yesterday = TODAY - timedelta(days=1)
    if TODAY not in sorted_marks and yesterday not in sorted_marks:
        return 0

    streak = 0
    current_date = TODAY

    if TODAY in sorted_marks:
        streak = 1
        current_date = TODAY - timedelta(days=1)
    elif yesterday in sorted_marks:
        streak = 1
        current_date = yesterday - timedelta(days=1)

    while current_date in sorted_marks:
        streak += 1
        current_date -= timedelta(days=1)

    return streak


def get_all_habits_with_details() -> List[dict]:
    habits = []
    for habit in habits_db.values():
        habit.streak = calculate_streak(habit.marks)
        habits.append({
            'id': habit.id,
            'name': habit.name,
            'marks': habit.marks,
            'streak': habit.streak
        })
    return sorted(habits, key=lambda h: h['id'])


def get_habit_by_id_with_details(habit_id: int) -> dict | None:
    habit = habits_db.get(habit_id)
    if habit is None:
        return None

    habit.streak = calculate_streak(habit.marks)
    return {
        'id': habit.id,
        'name': habit.name,
        'marks': habit.marks,
        'streak': habit.streak
    }


def create_habit(habit_data) -> Habit:
    global next_habit_id

    name = habit_data.name if hasattr(habit_data, 'name') else habit_data
    if not name or not name.strip():
        raise ValueError("Habit name cannot be empty.")

    for h in habits_db.values():
        if h.name.lower() == name.strip().lower():
            raise ValueError("Habit with this name already exists.")

    habit = Habit(id=next_habit_id, name=name.strip())
    habits_db[next_habit_id] = habit
    next_habit_id += 1
    return habit


def update_habit(habit_id: int, habit_data) -> Habit | None:
    habit = habits_db.get(habit_id)
    if habit is None:
        return None

    name = habit_data.name if hasattr(habit_data, 'name') else habit_data
    if not name or not name.strip():
        raise ValueError("Habit name cannot be empty.")

    for h in habits_db.values():
        if h.id != habit_id and h.name.lower() == name.strip().lower():
            raise ValueError("Habit with this name already exists.")

    habit.name = name.strip()
    return habit


def delete_habit(habit_id: int) -> bool:
    if habit_id in habits_db:
        del habits_db[habit_id]
        return True
    return False


def mark_habit(habit_id: int) -> dict | None:
    habit = habits_db.get(habit_id)
    if habit is None:
        return None

    if TODAY in habit.marks:
        raise ValueError("Habit already marked for today.")

    habit.marks.append(TODAY)
    habit.streak = calculate_streak(habit.marks)

    return {
        'id': habit.id,
        'name': habit.name,
        'last_marked_at': TODAY,
        'streak': habit.streak
    }


def is_habit_marked_today(habit_id: int) -> bool:
    habit = habits_db.get(habit_id)
    return habit is not None and TODAY in habit.marks


def get_all_habits() -> List[Habit]:
    return list(habits_db.values())
