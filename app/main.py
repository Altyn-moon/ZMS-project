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
#admin arai
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, models
from app.database import get_db, engine
from app.routes import work_orders
from app.routes import documents
from app.schemas import WorkOrderCreate, WorkOrderRead
from fastapi import APIRouter

# Создание всех таблиц
models.Base.metadata.create_all(bind=engine)

# Создание приложения
app = FastAPI()

# Маршрут для создания WorkOrder
@app.post("/api/workorders", response_model=schemas.WorkOrderRead)
def create_work_order(order: schemas.WorkOrderCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_work_order(db, order)
    except Exception as e:
        print("❌ Ошибка при создании WorkOrder:", str(e))
        raise HTTPException(status_code=500, detail=str(e))

# Маршрут для создания полной структуры WorkOrder + WorkCard + Operations + Documents
@app.post("/api/full-workorder")
def create_full_workorder(data: schemas.FullWorkOrder, db: Session = Depends(get_db)):
    return crud.create_full_workorder(db, data)


# Подключение маршрутов
app.include_router(work_orders.router)
app.include_router(documents.router)




templates = Jinja2Templates(directory="app/templates")



# altush
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
