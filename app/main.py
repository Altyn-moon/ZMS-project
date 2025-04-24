from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.routes import auth  # <-- вот здесь без точки!
from fastapi.responses import FileResponse
import os

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
<<<<<<< HEAD
def login_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "message": ""})
"""
@app.post("/login", response_class=HTMLResponse)
def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.login == username, User.password == password).first()
    if user:
        response = RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)
        response.set_cookie(key="user_role", value=user.role)
        response.set_cookie(key="username", value=user.name)  # user.name вместо user.username
        return response
    else:
        # Возвращаем форму логина с сообщением и флагом, чтобы показать логин
        return templates.TemplateResponse("index.html", {
            "request": request,
            "message": "Неверный логин или пароль",
            "force_login_screen": True
        })"""
    
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
=======
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
>>>>>>> f55692a7ffb55e64933b76441746aa07bf5e5266

app.include_router(auth.router)

#from app.database import engine
#from app.models import Base

#Base.metadata.create_all(bind=engine)

<<<<<<< HEAD
"""@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    user_name = request.cookies.get("username", "Гость")
    print(f"👤 Имя пользователя из cookie: {user_name}")  # Добавила
=======
@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    user_name = "Иванов Иван"  # потом заменим на реального пользователя
>>>>>>> f55692a7ffb55e64933b76441746aa07bf5e5266
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
    })"""

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

@app.get("/pdfs/{pdf_name}", response_class=FileResponse)
async def get_pdf(pdf_name: str):
    pdf_path = os.path.join("app/static/pdfs", pdf_name)
    if os.path.exists(pdf_path):
        return FileResponse(pdf_path, media_type='application/pdf')
    return {"error": "PDF не найден"}