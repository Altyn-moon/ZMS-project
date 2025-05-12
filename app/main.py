
from fastapi import FastAPI, Form, Request, status, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()


# Подключаем статику и шаблоны
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")
# === Главная страница (при нажатии лого админ)
@app.get("/admin_dashboard", response_class=HTMLResponse)
def admin_dashboard(request: Request):
    return templates.TemplateResponse("admin_dashboard.html", {"request": request})
'''# === Выйти (админ)
@app.post("/logout")
def logout(response: Response):
    response.delete_cookie("session")
    # либо сразу редирект
    return RedirectResponse(url="/login", status_code=303)'''
# === Главная страница (логин для всех)

from fastapi import FastAPI, Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from pydantic import BaseModel
from typing import List
from starlette.requests import Request
import sqlite3
import enum

from sqlalchemy.orm import Session
from fastapi import status
from pydantic import BaseModel

from app import crud, schemas

from app.database import SessionLocal
from app.models import User, UserRole

from app.database import Base, engine
from app.routes.admin import router as admin_router
from app.routes.users import router as users_router
from app.routes import auth, admin

# 1) Создаём все таблицы (если ещё не созданы)
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(admin_router)
app.include_router(users_router, prefix="/users")

from fastapi import Form, Request, APIRouter, Depends
from fastapi.responses import RedirectResponse

router = APIRouter()

# 2) «Статика» и шаблоны
# Настроим сервер для обслуживания статических файлов, включая PDF
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# 3) Депенденси для работы с БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 4) Форма логина (GET)
@app.get("/", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "message": ""
    })


# === Логин по умолчанию (админ)
@app.post("/login", response_class=HTMLResponse)
def login(request: Request):
    response = RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="user_role", value="admin")
    return response

# === Дэшборд для администратора
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    try:
        user_name = request.cookies.get("username", "Админ")
        work_items = [
            {"id": 1, "name": "Изготовление переводника", "client": "ТОО «СБП» Казмунайгаз-Бурение", "job_num": "1135-24"},
            {"id": 2, "name": "Втулка для шарнира", "client": "ТШО", "job_num": "1136-24"},
            {"id": 3, "name": "Гайка шарнира (левая резьба) для бурового оборудования", "client": "ТШО", "job_num": "1137-24"},
            {"id": 4, "name": "Изготовление переводника", "client": "ТОО «СБП» Казмунайгаз-Бурение", "job_num": "1138-24"},
            {"id": 5, "name": "Втулка для шарнира", "client": "ТШО", "job_num": "1139-24"},
            {"id": 6, "name": "Изготовление переводника", "client": "ТОО «СБП» Казмунайгаз-Бурение", "job_num": "1140-24"},
            {"id": 7, "name": "Втулка для шарнира", "client": "ТШО", "job_num": "1141-24"},
            {"id": 8, "name": "Гайка шарнира (левая резьба) для бурового оборудования", "client": "ТШО", "job_num": "1142-24"},
            {"id": 9, "name": "Гайка шарнира (левая резьба) для бурового оборудования", "client": "ТШО", "job_num": "1143-24"},
            {"id": 10, "name": "Втулка для шарнира", "client": "ТШО", "job_num": "1144-24"},
        ]
        return templates.TemplateResponse("dashboard.html", {
            "request": request,
            "user_name": user_name,
            "work_items": work_items
        })
    except Exception as e:
        print(f"❌ Ошибка на дэшборде админа: {e}")
        return HTMLResponse(content="Ошибка на сервере.", status_code=500)

# === Логин для администратора (отдельная форма)
@app.post("/admin/login")
async def admin_login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
):
    if username == "admin" and password == "1234":
        response = RedirectResponse(url="/dashboard", status_code=302)
        return response
    return templates.TemplateResponse("admin_login.html", {"request": request, "error": "Неверный логин или пароль"})

# 5) Обработка логина (POST)
@app.post("/login", response_class=HTMLResponse)
def do_login(
    request: Request,
    login:    str    = Form(...),
    password: str    = Form(...),
    db:       Session = Depends(get_db)
):
    user = (
        db.query(User)
          .filter(
            User.login    == login,
            User.password == password
          )
          .first()
    )
    if not user:
        # неверные учётные — снова форма с ошибкой
        return templates.TemplateResponse("index.html", {
            "request": request,
            "message": "Неверный логин или пароль"
        })

    """# определяем, куда редиректить
    role = user.role.value if isinstance(user.role, enum.Enum) else user.role
    if role == UserRole.admin.value:
        target = "/admin/dashboard"
    elif role == UserRole.inspector.value:
        target = "/inspector/dashboard"
    else:
        target = "/dashboard"""

    # выбираем куда редиректить
    role = user.role.value
    if role == UserRole.admin.value:
        target = "/admin/dashboard"
    elif role == UserRole.inspector.value:
        target = "/inspector/dashboard"
    else:  # worker и все остальные
        target = "/dashboard"

    # редирект + сохраняем ФИО в cookie
    response = RedirectResponse(url=target, status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="username", value=user.name)
    return response

# 6) Дашборд рабочего цеха (worker)
@app.get("/dashboard", response_class=HTMLResponse)
def worker_dashboard(request: Request):
    user_name = request.cookies.get("username", "Гость")
    # сюда потом вытянем реальные work_items из БД
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "user_name": user_name,
        "work_items": []
    })

# 7) Дашборд инспектора
@app.get("/inspector/dashboard", response_class=HTMLResponse)
def inspector_dashboard(request: Request):
    user_name = request.cookies.get("username", "Гость")
    return templates.TemplateResponse("inspector_dashboard.html", {
        "request": request,
        "user_name": user_name,
        # ... можно передать список заявок, которые инспектор видит
    })


# 8) Дашборд администратора
@app.get("/admin/dashboard", response_class=HTMLResponse)

async def admin_dashboard(request: Request):
    return templates.TemplateResponse("admin_dashboard.html", {"request": request})

# === Логин-страница инспектора
@app.get("/inspector/login", response_class=HTMLResponse)
async def inspector_login_form(request: Request):
    return templates.TemplateResponse("inspector_login.html", {"request": request, "error": ""})

# === Логин-инспектора (обработка формы)
@app.post("/inspector/login")
async def inspector_login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
):
    if username == "inspector" and password == "1234":
        response = RedirectResponse(url="/inspector/dashboard", status_code=302)
        response.set_cookie(key="username", value=username)
        return response
    return templates.TemplateResponse("inspector_login.html", {"request": request, "error": "Неверный логин или пароль"})

@app.get("/inspector/dashboard", response_class=HTMLResponse)
async def inspector_dashboard(request: Request):
    try:
        user_name = request.cookies.get("username", "Инспектор")

        work_items = [
            {"id": 1, "name": "Изготовление переводника", "client": "ТОО «СБП» Казмунайгаз-Бурение", "job_num": "1135-24"},
            {"id": 2, "name": "Втулка для шарнира", "client": "ТШО", "job_num": "1136-24"},
            {"id": 3, "name": "Гайка шарнира (левая резьба) для бурового оборудования", "client": "ТШО", "job_num": "1137-24"},
            {"id": 4, "name": "Изготовление переводника", "client": "ТОО «СБП» Казмунайгаз-Бурение", "job_num": "1138-24"},
            {"id": 5, "name": "Втулка для шарнира", "client": "ТШО", "job_num": "1139-24"},
            {"id": 6, "name": "Изготовление переводника", "client": "ТОО «СБП» Казмунайгаз-Бурение", "job_num": "1140-24"},
            {"id": 7, "name": "Втулка для шарнира", "client": "ТШО", "job_num": "1141-24"},
            {"id": 8, "name": "Гайка шарнира (левая резьба) для бурового оборудования", "client": "ТШО", "job_num": "1142-24"},
            {"id": 9, "name": "Гайка шарнира (левая резьба) для бурового оборудования", "client": "ТШО", "job_num": "1143-24"},
            {"id": 10, "name": "Втулка для шарнира", "client": "ТШО", "job_num": "1144-24"},
        ]

        return templates.TemplateResponse("inspector_dashboard.html", {
            "request": request,
            "user_name": user_name,
            "work_items": work_items
        })

    except Exception as e:
        print(f"❌ Ошибка на дэшборде инспектора: {e}")
        return HTMLResponse(content="Ошибка на сервере.", status_code=500)

def admin_dashboard(request: Request):
    user_name = request.cookies.get("username", "Гость")
    return templates.TemplateResponse("admin_dashboard.html", {
        "request": request,
        "user_name": user_name,
        # ... можно передать список всех юзеров, заявок и т.д.
    })

