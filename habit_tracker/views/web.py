from fastapi import APIRouter, Request, status
from habit_tracker.core import services
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import os
from habit_tracker.core.models import HabitCreate, HabitUpdate

current_dir = os.path.dirname(__file__)
templates_dir = os.path.join(current_dir, "..", "templates")
templates = Jinja2Templates(directory=templates_dir)

router = APIRouter()

@router.get("/", name="main-page", response_class=HTMLResponse)
def show_list(request: Request):
    habits = services.get_all_habits()
    habits_with_details = [
        {
            "id": habit.id,
            "name": habit.name,
            "streak": services.calculate_streak(habit.marks),
            "marked_today": services.TODAY in habit.marks
        }
        for habit in habits
    ]
    context = {
        "request": request,
        "habits": habits_with_details
    }
    return templates.TemplateResponse("index.html", context=context)


@router.get("/habit/{habit_id}/", name="habit-detail", response_class=HTMLResponse)
def show_detail_habit(request: Request, habit_id: int):
    habit = services.get_habit_by_id(habit_id)
    habit_detail = {
        "id": habit.id,
        "name": habit.name,
        "marks": habit.marks,
        "streak": services.calculate_streak(habit.marks)
    }
    context = {
        "request": request,
        "habit": habit_detail
    }
    return templates.TemplateResponse("habit_detail.html", context=context)


@router.post("/habit/add/", name="add_habit_from_form", response_class=RedirectResponse)
async def add_habit_from_form(request: Request):
    form = await request.form()
    name = form.get("name")
    habit_data = HabitCreate(name=name)
    services.create_habit(habit_data)
    return RedirectResponse(url=router.url_path_for("main-page"), status_code=status.HTTP_303_SEE_OTHER)


@router.post("/habit/{habit_id}/mark", name="mark_habit_from_form", response_class=RedirectResponse)
def mark_habit(request: Request, habit_id: int):
    services.mark_habit_completed(habit_id)
    return RedirectResponse(url=router.url_path_for("main-page"), status_code=status.HTTP_303_SEE_OTHER)


@router.post("/habit/{habit_id}/edit", name="edit_habit_from_form", response_class=RedirectResponse)
async def edit_habit_name(request: Request, habit_id: int):
    form = await request.form()
    name = form.get("name")
    habit_data = HabitUpdate(name=name)
    services.update_habit(habit_id, habit_data)
    return RedirectResponse(url=router.url_path_for("habit-detail", habit_id=habit_id), status_code=status.HTTP_303_SEE_OTHER)


@router.post("/habit/{habit_id}/delete", name="delete_habit_from_form", response_class=RedirectResponse)
def delete_habit_endpoint(request: Request, habit_id: int):
    services.delete_habit(habit_id)
    return RedirectResponse(url=router.url_path_for("main-page"), status_code=status.HTTP_303_SEE_OTHER)


@router.get("/stats/", name="stats-page", response_class=HTMLResponse)
def get_stats_page(request: Request):
    habits = services.get_all_habits()
    stats_data = []
    for habit in habits:
        stats = services.calculate_habit_stats(habit)
        habit_stats = {
            "id": habit.id,
            "name": habit.name,
            **stats
        }
        stats_data.append(habit_stats)

    context = {
        "request": request,
        "stats": stats_data
    }
    return templates.TemplateResponse("stats.html", context=context)


