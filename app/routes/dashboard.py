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
                    "work_times": times_data,
                    "documents_id": op.documents_id,
                })
            cards_data.append({
                "id": card.id,
                "title": card.title,
                "material": card.material,
                "cast_number": card.cast_number,
                "operation_descriptions": ops_data,
                "documents_id": card.documents_id,
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
