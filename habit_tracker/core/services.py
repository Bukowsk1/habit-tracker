from datetime import date, timedelta
from habit_tracker.core.models import Habit, HabitUpdate, HabitCreate
from habit_tracker.core.exceptions import HabitAlreadyMarkedTodayException, HabitNameConflictException, HabitNotFoundException, InvalidInputException

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
        raise InvalidInputException(detail="Habit name cannot be empty.")

    for habit in habits_db.values():
        if habit_data.name == habit.name:
            raise HabitNameConflictException()

    new_habit = Habit(
        id=next_habit_id,
        name=habit_data.name
    )
    habits_db[next_habit_id] = new_habit
    next_habit_id += 1
    return new_habit


def mark_habit_completed(habit_id: int) -> Habit:
    """Отметить выполнение привычки за текущий день."""
    habit = get_habit_by_id(habit_id)

    date_today = TODAY
    if date_today in habit.marks:
        raise HabitAlreadyMarkedTodayException()

    habit.marks.append(date_today)
    return habit


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
    

def get_all_habits() -> list[Habit]:
    """Возвращает список всех привычек."""
    return list(habits_db.values())


def calculate_max_streak(marks: list[date]) -> int:
    """Рассчитывает максимальный streak (серию последовательных дней) за всё время."""
    if not marks:
        return 0

    unique_marks = sorted(set(marks))
    max_streak = 0
    current_streak = 1

    for i in range(1, len(unique_marks)):
        if (unique_marks[i] - unique_marks[i-1]).days == 1:
            current_streak += 1
        else:
            max_streak = max(max_streak, current_streak)
            current_streak = 1

    max_streak = max(max_streak, current_streak)
    return max_streak


def calculate_habit_stats(habit: Habit) -> dict:
    """Рассчитывает полную статистику по привычке."""
    total_marks = len(habit.marks)
    current_streak = calculate_streak(habit.marks)
    max_streak = calculate_max_streak(habit.marks)

    # Расчет success_rate
    if not habit.marks:
        success_rate = 0.0
    else:
        first_mark = min(habit.marks)
        days_since_start = (TODAY - first_mark).days + 1
        success_rate = round((total_marks / days_since_start) * 100, 2)

    # Последние 5 дат в обратном порядке
    last_dates = sorted(habit.marks, reverse=True)[:5]

    return {
        "total_marks": total_marks,
        "current_streak": current_streak,
        "max_streak": max_streak,
        "success_rate": success_rate,
        "last_dates": last_dates
    } 


def update_habit(habit_id: int, habit_data: HabitUpdate) -> Habit:
    """Обновляет привычку."""
    habit = get_habit_by_id(habit_id)

    habit_data_name = habit_data.name.strip()

    if len(habit_data_name) == 0:
        raise InvalidInputException(detail="Habit name cannot be empty.")

    if habit_data_name == habit.name:
        return habit

    for h in habits_db.values():
        if habit_data_name == h.name:
            raise HabitNameConflictException()

    habit.name = habit_data_name
    return habit
    
    
def delete_habit(habit_id: int) -> None:
    """Удаляет привычку."""
    get_habit_by_id(habit_id)  # Проверит существование и выбросит исключение если нет
    habits_db.pop(habit_id)
        

def get_habit_by_id(habit_id: int) -> Habit:
    """Возвращает привычку по ID."""
    habit = habits_db.get(habit_id)
    if habit is None:
        raise HabitNotFoundException()
    return habit






    
        

        
        