from datetime import date, timedelta
from habit_tracker.core.models import Habit, HabitUpdate, HabitCreate

TODAY = date(2025, 7, 12)

habits_db: dict[int, Habit] = {    
    1: Habit(id=1, name="Бег", marks=[date(2025, 7, 10), date(2025, 7, 11)]),    
    2: Habit(id=2, name="Чтение", marks=[date(2025, 7, 11)]),    
    3: Habit(id=3, name="Медитация", marks=[])}

next_habit_id = 4


def create_habit(habit_data: HabitCreate) -> Habit:
    """Создать новую привычку."""
    global next_habit_id

    if len(habit_data.name.strip()) == 0:
        raise ValueError("Название привычки не может быть пустым.")

    for habit in habits_db.values():
        if habit_data.name == habit.name:
            raise ValueError("Привычка с таким называнием уже существует.")

    new_habit = Habit(
        id=next_habit_id,
        name=habit_data.name
    )
    habits_db[next_habit_id] = new_habit
    next_habit_id += 1
    return new_habit


def mark_habit(habit_id: int) -> dict | None:
    """Отметить выполнение привычки за текущий день."""
    habit = habits_db.get(habit_id, None)
    if habit is None:
        return None

    date_today = TODAY
    if date_today in habit.marks:
        raise ValueError("Привычка уже отмечена за сегодня.")
    
    habit.marks.append(date_today)
    marked_habit = {
        "id": habit_id,
        "name": habit.name,
        "last_marked_at": date_today,
        "streak": calculate_streak(habit.marks)
    }
    return marked_habit


def calculate_streak(marks: list[date]) -> int:

    if not marks:
        return 0

    unique_marks: set[date] = set[date](marks)
    streak = 0
    
    yesterday = TODAY - timedelta(days=1)
    
    is_marked_today = TODAY in unique_marks
    is_marked_yesterday = yesterday in unique_marks
    
    if not is_marked_today and not is_marked_yesterday:
        return 0
    
    if is_marked_today:
        streak = 1
        current_day = TODAY
    elif is_marked_yesterday:
        streak = 1
        current_day = yesterday
    else:
        return 0
    day_to_check = current_day - timedelta(days=1)
    
    while day_to_check in unique_marks:
        streak += 1
        day_to_check -= timedelta(days=1)
        
    return streak
    

def get_all_habits_with_details() -> list[dict]:
    habits_list = []
    for h in habits_db.values():
        habit = {
            "id": h.id,
            "name": h.name,
            "marks": h.marks,
            "streak": calculate_streak(h.marks)
        }
        habits_list.append(habit)

    return sorted(habits_list, key=lambda x: x["id"]) 


def update_habit(habit_id: int, habit_data: HabitUpdate) -> Habit | None:
    if habit_id not in habits_db:
        return None

    habit = habits_db[habit_id]
    habit_data_name = habit_data.name.strip()
    
    if len(habit_data_name) == 0:
        raise ValueError("Название привычки не может быть пустым.")

    if habit_data_name == habit.name:
        return habit

    for h in habits_db.values():
        if habit_data_name == h.name:
            raise ValueError("Привычка с таким названием уже существует.")
            
    habit.name = habit_data_name
    return habit
    
    
def delete_habit(habit_id: int) -> bool:
    if habits_db.pop(habit_id, None) is None:
        return False
    return True
        

def is_habit_marked_today(habit_id: int) -> bool:
    habit = habits_db.get(habit_id, None)

    if habit is None:
        return False

    if TODAY in habit.marks:
        return True
    return False


def get_habit_by_id_with_details(habit_id: int) -> dict | None:
    habit = habits_db.get(habit_id, None)
    if habit is None:
        return None
    habit_dict = {
        "id": habit_id,
        "name": habit.name,
        "marks": habit.marks,
        "streak": calculate_streak(habit.marks)
    }
    return habit_dict






    
        

        
        