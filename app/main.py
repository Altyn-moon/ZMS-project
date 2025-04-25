from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Настроим сервер для обслуживания статических файлов, включая PDF
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.mount("/pdfs", StaticFiles(directory="app/static/pdfs"), name="pdfs")

templates = Jinja2Templates(directory="app/templates")

# Статическая страница с кнопкой для входа
@app.get("/", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "message": ""})

# При нажатии на кнопку "Вход" редиректим на дэшборд
@app.post("/login", response_class=HTMLResponse)
def login(request: Request):
    return RedirectResponse(url="/dashboard", status_code=302)

# Дэшборд
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    user_name = "Асель"  # Простой текст без авторизации
    # Пример работы с задачами для дэшборда
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

@app.get("/logout")
def logout():
    # Тут можно очистить сессии или куки, если требуется
    return RedirectResponse(url="/", status_code=303)

# Страница с видеоинструкциями
@app.get("/instructions", response_class=HTMLResponse)
def instructions(request: Request):
    return templates.TemplateResponse("instructions.html", {"request": request})