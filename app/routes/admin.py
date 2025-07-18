from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models import User, UserRole

router = APIRouter(prefix="/admin", tags=["admin"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/login", response_class=HTMLResponse)
def show_login(request: Request):
    return templates.TemplateResponse("admin_login.html", {"request": request})


@router.post("/login", response_class=HTMLResponse)
def do_login(
    request: Request,
    login: str    = Form(...),
    password: str = Form(...),
    db: Session   = Depends(get_db)
):
    user = (
        db
        .query(User)
        .filter(
            User.login    == login,
            User.password == password,
            User.role     == UserRole.admin
        )
        .first()
    )
    if not user:
        return templates.TemplateResponse(
            "admin_login.html",
            {"request": request, "error": "Неверный логин или пароль"}
        )

    resp = RedirectResponse("/admin/dashboard", status_code=status.HTTP_302_FOUND)
    resp.set_cookie("username", user.name)
    return resp


@router.get("/dashboard", response_class=HTMLResponse)
def admin_dashboard(request: Request):
    user_name = request.cookies.get("username", "Админ")
    return templates.TemplateResponse(
        "admin_dashboard.html",
        {"request": request, "user_name": user_name}
    )
