from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from habit_tracker.core.services import (
    get_all_habits_with_details,
    get_habit_by_id_with_details,
    create_habit,
    update_habit,
    delete_habit,
    mark_habit,
    is_habit_marked_today,
)

router = APIRouter()
templates = Jinja2Templates(directory="habit_tracker/templates")


@router.get("/", name="main-page")
async def main_page(request: Request):
    habits = get_all_habits_with_details()
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "habits": habits,
            "is_marked_today": is_habit_marked_today
        }
    )


@router.get("/habit/{habit_id}/", name="habit-detail")
async def habit_detail(request: Request, habit_id: int):
    habit = get_habit_by_id_with_details(habit_id)
    if habit is None:
        raise HTTPException(status_code=404, detail="Habit not found")
    return templates.TemplateResponse(
        "habit_detail.html",
        {"request": request, "habit": habit}
    )


@router.post("/habit/add", name="add_habit_from_form")
async def add_habit_from_form(name: str = Form(...)):
    try:
        create_habit(name)
    except ValueError:
        pass
    return RedirectResponse(url=router.url_path_for("main-page"), status_code=303)


@router.post("/habit/{habit_id}/mark", name="mark_habit_from_form")
async def mark_habit_from_form(habit_id: int):
    try:
        mark_habit(habit_id)
    except (ValueError, TypeError):
        pass
    return RedirectResponse(url=router.url_path_for("main-page"), status_code=303)


@router.post("/habit/{habit_id}/edit", name="edit_habit_from_form")
async def edit_habit_from_form(habit_id: int, name: str = Form(...)):
    try:
        update_habit(habit_id, name)
    except ValueError:
        pass
    return RedirectResponse(
        url=router.url_path_for("habit-detail", habit_id=habit_id),
        status_code=303
    )


@router.post("/habit/{habit_id}/delete", name="delete_habit_from_form")
async def delete_habit_from_form(habit_id: int):
    delete_habit(habit_id)
    return RedirectResponse(url=router.url_path_for("main-page"), status_code=303)
