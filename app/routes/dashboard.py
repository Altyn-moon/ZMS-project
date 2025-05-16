"""from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session, joinedload
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from app import models
from app.models import WorkCard
from app.schemas import WorkOrderOut
from app.dependencies import get_db

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/dashboard", response_class=HTMLResponse)
def get_dashboard(
    request: Request,
    db: Session = Depends(get_db),
):
    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")

    user = db.query(models.User).filter_by(id=user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

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
            "name":       order.description,
            "customer":   order.customer,
            "code":       order.work_order_number,
            "work_cards": cards_data,
        })

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "user_name": user.name,
        "user_id": user.id,
        "orders_data": orders_data
    })


@router.get("/work_cards/{order_id}")
def get_work_cards(order_id: int, db: Session = Depends(get_db)):
    cards = db.query(WorkCard).filter(WorkCard.work_order_id == order_id).all()
    print(f"Cards for order {order_id}:", cards)
    return [
        {
            "id": c.id,
            "name": c.title,
            "description": c.job_description
        } for c in cards
    ]

@router.get("/api/orders_deep/{order_id}", response_model=WorkOrderOut)
def get_full_order(order_id: int, db: Session = Depends(get_db)):
    order = (
        db.query(models.WorkOrder)
        .options(
            joinedload(models.WorkOrder.work_cards)
            .joinedload(models.WorkCard.operation_descriptions)
            .joinedload(models.OperationDescription.work_times)
        )
        .filter(models.WorkOrder.id == order_id)
        .first()
    )
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

"""

# ─── Обновлённый dashboard.py ─────────────────────────────
from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session, joinedload
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from app import models
from app.models import WorkCard
from app.schemas import WorkOrderOut
from app.dependencies import get_db

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/dashboard", response_class=HTMLResponse)
def get_dashboard(
    request: Request,
    db: Session = Depends(get_db),
):
    user_id = request.session.get("user_id")
    user_name = request.session.get("user_name", "Гость")

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
                for wt in op.work_times:
                    times_data.append({
                        "id": wt.id,
                        "user": wt.user.name if wt.user else "",
                        "start_time": wt.start_time.isoformat() if wt.start_time else "",
                        "end_time": wt.end_time.isoformat() if wt.end_time else "",
                    })
                ops_data.append({
                    "id": op.id,
                    "operation": op.operation,
                    "equipment": op.equipment,
                    "instruction_code": op.instruction_code,
                    "instruction_file_url": op.instruction_file_url,
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
            "description": order.description,
            "customer": order.customer,
            "work_order_number": order.work_order_number,
            "work_cards": cards_data,
        })

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "user_name": user_name,
        "user_id": user_id,
        "orders_data": orders_data
    })
