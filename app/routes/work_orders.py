from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud
from app.database import get_db
from app.schemas import WorkOrderCreate, WorkOrderRead
from app.models import WorkOrder
from app.models import Document

from fastapi import File, UploadFile, Form
from app.models import Document
from datetime import datetime
from app import models


router = APIRouter()

@router.post("/api/workorders", response_model=WorkOrderRead)
def create_work_order(work_order: WorkOrderCreate, db: Session = Depends(get_db)):
    db_work_order = WorkOrder(**work_order.dict())
    db.add(db_work_order)
    db.commit()
    db.refresh(db_work_order)
    return db_work_order

@router.post("/api/workcards")
def create_work_card(data: schemas.WorkCardCreate, db: Session = Depends(get_db)):
    db_card = models.WorkCard(**data.dict())
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card

router = APIRouter(prefix="/api")

@router.post("/api/documents")
async def upload_document(
    file: UploadFile = File(...),
    number: str = Form(...),
    work_card_id: int = Form(...),
    db: Session = Depends(get_db)
):
    try:
        content = await file.read()

        new_doc = Document(
            work_card_id=work_card_id,
            type="Drawing",  # или "Certificate" если нужно
            number=number,
            pdf_file=content,
            url=file.filename,
            created_at=datetime.utcnow()
        )
        db.add(new_doc)
        db.commit()
        db.refresh(new_doc)
        return {"message": "Файл загружен", "id": new_doc.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/api/full-workorder")
def create_full_workorder(data: schemas.FullWorkOrder, db: Session = Depends(get_db)):
    # Создать заказ
    work_order = models.WorkOrder(**data.work_order.dict())
    db.add(work_order)
    db.commit()
    db.refresh(work_order)

    # Создать карту
    card_data = data.work_card.dict()
    card_data["work_order_id"] = work_order.id
    work_card = models.WorkCard(**card_data)
    db.add(work_card)
    db.commit()
    db.refresh(work_card)

    # Создать операции
    for op in data.operations:
        db_op = models.OperationDescription(work_card_id=work_card.id, **op.dict())
        db.add(db_op)

    db.commit()
    return {"message": "Успешно сохранено"}
from fastapi import UploadFile, File, Form

@router.post("/full-workorder")
async def create_full_workorder(
    data: str = Form(...),
    pdf_file: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    parsed = json.loads(data)
    # Дальше логика сохранения parsed и файла pdf_file



# маршрут для отображения данных на главной странице администратора
print("📦 Модуль work_orders загружен")

from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session, joinedload
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.database import get_db
from app.models import WorkOrder

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/admin/dashboard", response_class=HTMLResponse)
def show_admin_dashboard(request: Request, db: Session = Depends(get_db)):
    user_name = request.cookies.get("username", "Админ")

    print("🟢 show_admin_dashboard вызван!")
    work_orders = db.query(WorkOrder).order_by(WorkOrder.created_at.desc()).all()

    print("Найдено заказов:", len(work_orders))
    for o in work_orders:
        print("ID заказа:", o.id)

    return templates.TemplateResponse("admin_dashboard.html", {
        "request": request,
        "work_orders": work_orders,
        "user_name": user_name
    })

@router.get("/admin/dashboard", response_class=HTMLResponse)
def show_dashboard(request: Request, db: Session = Depends(get_db)):
    work_orders = db.query(models.WorkOrder).order_by(models.WorkOrder.created_at.desc()).all()
    return templates.TemplateResponse("admin_dashboard.html", {
        "request": request,
        "work_orders": work_orders,
        "mode": "list",  # ← добавили
        "user_name": request.cookies.get("username", "Админ")
    })


@router.get("/admin/workorder/{order_id}", response_class=HTMLResponse)
def view_work_order(order_id: int, request: Request, db: Session = Depends(get_db)):
    work_order = db.query(models.WorkOrder).filter(models.WorkOrder.id == order_id).first()
    work_card = db.query(models.WorkCard).filter(models.WorkCard.work_order_id == order_id).first()
    operations = []
    if work_card:
        operations = db.query(models.OperationDescription).filter_by(work_card_id=work_card.id).all()

    return templates.TemplateResponse("admin_dashboard.html", {  # ← тот же шаблон
        "request": request,
        "order": work_order,
        "card": work_card,
        "operations": operations,
        "mode": "form",  # ← режим: форма
        "user_name": request.cookies.get("username", "Админ")
    })




