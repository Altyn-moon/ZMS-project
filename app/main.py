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

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas import WorkOrderOut
from app.schemas import WorkOrderCreate
from app.schemas import WorkCardOut
from app.schemas import WorkCardCreate

from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware


# Создание всех таблиц
models.Base.metadata.create_all(bind=engine)

# Создание приложения
app = FastAPI()


# Маршрут для создания WorkOrder

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#admin arai

from fastapi import APIRouter
from app.schemas import WorkOrderRead

router = APIRouter()

@app.get("/get-user-by-uid")
def get_user_by_uid(uid: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.uid == uid).first()
    if not user:
        raise HTTPException(status_code=404, detail="UID не найден")
    return {
        "login": user.login,
        "password": user.password,
        "role": user.role.value
    }

import threading
from app.pikalka import start_reader_loop

threading.Thread(target=start_reader_loop, daemon=True).start()


@app.post("/api/workorders", response_model=schemas.WorkOrderRead)
def create_work_order(order: schemas.WorkOrderCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_work_order(db, order)
    except Exception as e:
        print("❌ Ошибка при создании WorkOrder:", str(e))
        raise HTTPException(status_code=500, detail=str(e))

# Маршрут для создания полной структуры WorkOrder + WorkCard + Operations + Documents
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import schemas, crud
from app.database import get_db

router = APIRouter()

@router.post("/api/workorder")
def create_full_workorder(data: schemas.FullWorkOrder, db: Session = Depends(get_db)):
    return crud.create_full_workorder(db, data)



# Подключение маршрутов
app.include_router(work_orders.router)
app.include_router(documents.router)





#@router.post("/workcards/", response_model=schemas.WorkOrderRead)
#def create_work_order(workcard_data: schemas.WorkOrderCreate, db: Session = Depends(get_db)):
   # new_order = models.WorkOrder(**workcard_data.dict())


templates = Jinja2Templates(directory="app/templates")




    
app.include_router(work_orders.router, prefix="/api")

# Создание приложения
app = FastAPI()

#admin arai

from fastapi import APIRouter
from app.schemas import WorkOrderRead

router = APIRouter()

@app.post("/api/workorders", response_model=schemas.WorkOrderRead)
def create_work_order(order: schemas.WorkOrderCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_work_order(db, order)
    except Exception as e:
        print("❌ Ошибка при создании WorkOrder:", str(e))  # ← добавь это
        raise HTTPException(status_code=500, detail=str(e))


#@router.post("/workcards/", response_model=schemas.WorkOrderRead)
#def create_work_order(workcard_data: schemas.WorkOrderCreate, db: Session = Depends(get_db)):
   # new_order = models.WorkOrder(**workcard_data.dict())

   # db.add(new_order)
   # db.commit()
   # db.refresh(new_order)  # Без этого new_order будет None или пустым

   # return new_order

    
app.include_router(work_orders.router, prefix="/api")

from app.routes import documents
app.include_router(documents.router)

from app.routes import work_orders
app.include_router(work_orders.router)


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

"""@app.get("/dashboard", response_class=HTMLResponse)
def worker_dashboard(request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    user_name = request.session.get("user_name")"""

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db)):
    user_name = request.cookies.get("username", "Гость")
    user_id = request.cookies.get("user_id")

    if not user_id:
        return templates.TemplateResponse("index.html", {"request": request, "msg": "Сессия не найдена. Пожалуйста, войдите снова."})

    work_orders = (
        db.query(models.WorkOrder)
        .filter(models.WorkOrder.user_id == user_id)
        .options(
            joinedload(models.WorkOrder.work_cards)
            .joinedload(models.WorkCard.operation_descriptions)
            .joinedload(models.OperationDescription.work_times)
        )
        .all()
    )

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "user_name": user_name,
        "orders_data": work_orders,   # ← ПЕРЕДАЁМ ORM, НЕ СЛОВАРИ
        "user_id": user_id,
    })
"""
    # Загружаем заказы с вложенными рабочими картами и операциями
    work_orders = (
        db.query(models.WorkOrder)
        .filter(models.WorkOrder.user_id == user_id)
        .options(
            joinedload(models.WorkOrder.work_cards)
            .joinedload(models.WorkCard.operation_descriptions)
            .joinedload(models.OperationDescription.work_times)
        )
        .all()
    )

    orders_data = []
    for order in work_orders:
        cards_data = []
        for card in order.work_cards:
            ops_data = []
            for op in card.operation_descriptions:
                times_data = [{
                    "id": wt.id,
                    "user": wt.user.name if wt.user else "",
                    "start_time": wt.start_time.isoformat(),
                    "end_time": wt.end_time.isoformat(),
                } for wt in op.work_times]
                ops_data.append({
                    "id": op.id,
                    "operation": op.operation,
                    "equipment": op.equipment,
                    "work_times": times_data,
                })
            cards_data.append({
                "id": card.id,
                "title": card.title,
                "job_description": card.job_description,
                "operation_descriptions": ops_data,
            })
        orders_data.append({
            "id": order.id,
            "name": order.name,
            "customer": order.customer,
            "code": order.code,
            "work_cards": cards_data,
        })

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "user_name": user_name,
        "orders_data": orders_data,
        "work_orders": work_orders,
        "user_id": user_id,
    })"""


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

