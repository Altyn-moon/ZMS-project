from fastapi import FastAPI, Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Подключаем статику и шаблоны
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# === Главная страница (логин для всех)
@app.get("/", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "message": ""})

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

