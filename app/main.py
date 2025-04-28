from fastapi import FastAPI, Form, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from fastapi import status
from pydantic import BaseModel

from app import crud, schemas

from app.database import SessionLocal
from app.models import User

from app.database import Base, engine
Base.metadata.create_all(bind=engine)


app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

"""added"""
class UserCreate(BaseModel):
    name: str
    role: str
    login: str
    password: str
    uid: str
    job_title: str

@app.post("/users/")
def create_user(user: UserCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    sql = """
    INSERT INTO users (name, role, login, password, uid, job_title, created_time)
    VALUES (%s, %s, %s, %s, %s, %s, NOW())
    """
    cursor.execute(sql, (user.name, user.role, user.login, user.password, user.uid, user.job_title))
    conn.commit()
    conn.close()
    return {"message": "User created successfully!"}
"""end"""


@app.get("/", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "message": ""})
    
@app.post("/login", response_class=HTMLResponse)
def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    print(f"Получен логин: {username}, пароль: {password}")  # 👈 Лог
    user = db.query(User).filter(User.login == username, User.password == password).first()
    if user:
        print(f"✅ Пользователь найден: {user.login}, роль: {user.role}")  # 👈 Лог
        response = RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)
        response.set_cookie(key="user_role", value=user.role)
        response.set_cookie(key="username", value=user.name)
        return response
    else:
        print("❌ Неверные данные")  # 👈 Лог
        return templates.TemplateResponse("index.html", {
            "request": request,
            "message": "Неверный логин или пароль",
            "force_login_screen": True
        })

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    user_name = request.cookies.get("username", "Гость")  # cookie уже содержит ФИО
    print(f"👤 Имя пользователя из cookie: {user_name}")  # Лог для проверки
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

from fastapi import Form
from fastapi.responses import RedirectResponse

# === ВХОД ДЛЯ АДМИНА ===

@app.get("/admin/login", response_class=HTMLResponse)
async def admin_login_page(request: Request):
    return templates.TemplateResponse("admin_login.html", {"request": request})

@app.post("/admin/login")
async def admin_login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):
    # ВРЕМЕННАЯ ПРОВЕРКА (заменишь потом на проверку из БД)
    if username == "admin" and password == "1234":
        response = RedirectResponse(url="/admin/dashboard", status_code=302)
        return response
    return templates.TemplateResponse("admin_login.html", {"request": request, "error": "Неверный логин или пароль"})

@app.get("/admin/dashboard", response_class=HTMLResponse)
async def admin_dashboard(request: Request):
    return templates.TemplateResponse("admin_dashboard.html", {"request": request})

"""added from Altush"""
# ➕ Создать пользователя
@app.post("/users/", response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)

# 📄 Получить одного пользователя
@app.get("/users/{user_id}", response_model=schemas.UserOut)
def read_user(user_id: int, db: Session = Depends(get_db)):
    return crud.get_user(db=db, user_id=user_id)

# 📄 Получить всех пользователей
@app.get("/users/", response_model=list[schemas.UserOut])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_users(db=db, skip=skip, limit=limit)

# ✏️ Обновить пользователя
@app.put("/users/{user_id}", response_model=schemas.UserOut)
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    updated_user = crud.update_user(db, user_id, user)
    if updated_user is None:
        return {"error": "User not found"}
    return updated_user

# ❌ Удалить пользователя
@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    deleted_user = crud.delete_user(db, user_id)
    if deleted_user is None:
        return {"error": "User not found"}
    return {"message": "User deleted"}


