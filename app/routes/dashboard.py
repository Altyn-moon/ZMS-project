from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session, joinedload
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse

from app import models
from app.dependencies import get_db

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/dashboard", response_class=HTMLResponse)
def get_dashboard(
    request: Request,
    db: Session = Depends(get_db),
):
    work_orders = (
        db.query(models.WorkOrder)
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
                times_data = []
                # <-- вот этот кусок исправляем:
                for wt in op.work_times:
                    times_data.append({
                        "id":         wt.id,
                        "user":       wt.user.name,
                        "start_time": wt.start_time.isoformat(),
                        "end_time":   wt.end_time.isoformat(),
                    })
                ops_data.append({
                    "id":            op.id,
                    "operation":     op.operation,
                    "equipment":     op.equipment,
                    "work_times":    times_data,
                })
            cards_data.append({
                "id":                       card.id,
                "title":                    card.title,
                "job_description":          card.job_description,
                "operation_descriptions":   ops_data,
            })
        orders_data.append({
            "id":         order.id,
            "name":       order.name,
            "customer":   order.customer,
            "code":       order.code,
            "work_cards": cards_data,
        })

    return templates.TemplateResponse("dashboard.html", {
        "request":       request,
        "work_orders":   work_orders,
        "orders_data":   orders_data,    # <-- ключ в контексте шаблона
    })


"""@router.get("/api/work_cards/{order_id}", response_class=JSONResponse)
def get_work_cards(order_id: int, db: Session = Depends(get_db)):
    work_cards = (
        db.query(models.WorkCard)
        .filter(models.WorkCard.order_id == order_id)
        .all()
    )
    result = []
    for card in work_cards:
        result.append({
            "id": card.id,
            "title": card.title,
            "description": card.job_description,
        })
    return result"""

@router.get("/work_cards/{order_id}")
def get_work_cards(order_id: int, db: Session = Depends(get_db)):
    cards = db.query(WorkCard).filter(WorkCard.work_order_id == order_id).all()
    print(f"Cards for order {order_id}:", cards)
    return [
        {
            "id": c.id,
            "name": c.name,
            "description": c.description
        } for c in cards
    ]







