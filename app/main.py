"""
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
from sqlalchemy.orm import Session
from starlette.middleware.sessions import SessionMiddleware
import os

# Импорт внутренней логики
from app import crud, schemas
from app.database import SessionLocal, Base, engine
from app.models import User, UserRole
from app.routes.dashboard import router as dashboard_router
from app.routes.admin import router as admin_router
from app.routes.users import router as users_router
from app.routes.work import router as work_router
from app.routes import auth, admin

# Создание всех таблиц
Base.metadata.create_all(bind=engine)

# Создание приложения
app = FastAPI()

# Добавление middleware
SECRET_KEY = os.getenv("SECRET_KEY", "default-dev-key")  # Временно для dev
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

# Подключение роутеров
app.include_router(auth.router)
app.include_router(admin_router)
app.include_router(users_router, prefix="/users")
app.include_router(dashboard_router)
app.include_router(work_router)

# Подключение статических файлов
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.mount("/pdfs", StaticFiles(directory="app/static/pdfs"), name="pdfs")

# Шаблоны
templates = Jinja2Templates(directory="app/templates")

app.include_router(auth.router)
app.include_router(admin_router)
app.include_router(users_router, prefix="/users")
app.include_router(dashboard_router)  

router = APIRouter()

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

    # выбираем куда редиректить
    role = user.role.value
    if role == UserRole.admin.value:
        target = "/admin/dashboard"
    elif role == UserRole.inspector.value:
        target = "/inspector/dashboard"
    else:  # worker и все остальные
        target = "/dashboard"

    request.session["user_id"] = user.id
    request.session["user_name"] = user.name  # или user.full_name

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

@app.get("/get_work_cards/{order_id}")
def get_work_cards(order_id: int, db: Session = Depends(get_db)):
    cards = db.query(WorkCard).filter(WorkCard.work_order_id == order_id).all()
    return [{"id": c.id, "name": c.name, "description": c.description} for c in cards]

"""

from fastapi import FastAPI, Form, Request, Depends, status, APIRouter, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session
from starlette.middleware.sessions import SessionMiddleware
import os

# Импорт внутренней логики
from app import crud, schemas
from app.database import SessionLocal, Base, engine
from app.models import User, UserRole
from app.routes.dashboard import router as dashboard_router
from app.routes.admin import router as admin_router
from app.routes.users import router as users_router
from app.routes.work import router as work_router
from app.routes import auth, admin

# Создание всех таблиц
Base.metadata.create_all(bind=engine)

# Создание приложения
app = FastAPI()

# Добавление middleware
SECRET_KEY = os.getenv("SECRET_KEY", "default-dev-key")  # Временно для dev
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

# Подключение роутеров
app.include_router(auth.router)
app.include_router(admin_router)
app.include_router(users_router, prefix="/users")
app.include_router(dashboard_router)
app.include_router(work_router)

# Подключение статических файлов
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.mount("/pdfs", StaticFiles(directory="app/static/pdfs"), name="pdfs")

# Шаблоны
templates = Jinja2Templates(directory="app/templates")

app.include_router(auth.router)
app.include_router(admin_router)
app.include_router(users_router, prefix="/users")
app.include_router(dashboard_router)  

router = APIRouter()

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

    # выбираем куда редиректить
    role = user.role.value
    if role == UserRole.admin.value:
        target = "/admin/dashboard"
    elif role == UserRole.inspector.value:
        target = "/inspector/dashboard"
    else:  # worker и все остальные
        target = "/dashboard"

    request.session["user_id"] = user.id
    request.session["user_name"] = user.name  # или user.full_name

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
def admin_dashboard(request: Request):
    user_name = request.cookies.get("username", "Гость")
    return templates.TemplateResponse("admin_dashboard.html", {
        "request": request,
        "user_name": user_name,
        # ... можно передать список всех юзеров, заявок и т.д.
    })

@app.get("/get_work_cards/{order_id}")
def get_work_cards(order_id: int, db: Session = Depends(get_db)):
    cards = db.query(WorkCard).filter(WorkCard.work_order_id == order_id).all()
    return [{"id": c.id, "name": c.name, "description": c.description} for c in cards]

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

