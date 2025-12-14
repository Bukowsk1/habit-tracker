from fastapi import APIRouter, Request, HTTPException, status
from pydantic import ValidationError
from habit_tracker.core import services
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import os
from habit_tracker.core.models import HabitCreate, HabitUpdate
from datetime import date

current_dir = os.path.dirname(__file__)
templates_dir = os.path.join(current_dir, "..", "templates")
templates = Jinja2Templates(directory=templates_dir)

router = APIRouter()

@router.get("/", name="main-page", response_class=HTMLResponse)
def show_list(request: Request):
    habits = services.get_all_habits_with_details()
    context = {
        "request": request,
        "habits": habits,
        "is_marked_today": services.is_habit_marked_today
    }
    return templates.TemplateResponse("index.html", context=context)


@router.get("/habit/{habit_id}/", name="habit-detail", response_class=HTMLResponse)
def show_detail_habit(request: Request, habit_id: int):
    habit = services.get_habit_by_id_with_details(habit_id)
    if habit is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Привычка с таким id не найдена.")
    context = {
        "request": request,
        "habit": habit
    }
    return templates.TemplateResponse("habit_detail.html", context=context)


@router.post("/habit/add/", name="add_habit_from_form", response_class=RedirectResponse)
async def add_habit_from_form(request: Request):
    form = await request.form()
    name = form.get("name")
    habit_data = HabitCreate(
        name=name
    )
    try:
        services.create_habit(habit_data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return RedirectResponse(url=router.url_path_for("main-page"), status_code=status.HTTP_303_SEE_OTHER)


@router.post("/habit/{habit_id}/mark", name="mark_habit_from_form", response_class=RedirectResponse)
def mark_habit(request: Request, habit_id: int):
    try:
        marked_habit = services.mark_habit(habit_id)
        if marked_habit is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Привычка с таким id не найдена.")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return RedirectResponse(url=router.url_path_for("main-page"), status_code=status.HTTP_303_SEE_OTHER)


@router.post("/habit/{habit_id}/edit", name="edit_habit_from_form", response_class=RedirectResponse)
async def edit_habit_name(request: Request, habit_id: int):
    form = await request.form()
    name = form.get("name")
    try:
        habit = HabitUpdate(name=name)
        updated_habit = services.update_habit(habit_id, habit)
        if updated_habit is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=("Привычка с таким id не найдена."))
        
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return RedirectResponse(url=router.url_path_for("habit-detail", habit_id=habit_id), status_code=status.HTTP_303_SEE_OTHER)


@router.post("/habit/{habit_id}/delete", name="delete_habit_from_form", response_class=RedirectResponse)
def delete_habit(request: Request, habit_id: int):
    is_deleted = services.delete_habit(habit_id)
    if is_deleted:
        return RedirectResponse(url=router.url_path_for("main-page"), status_code=status.HTTP_303_SEE_OTHER)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Привычка с таким id не найдена.")


