from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.models import WorkOrder, WorkCard, OperationDescription, WorkTime

router = APIRouter(prefix="/api")

# ==== МАРШРУТЫ ДЛЯ WORK ORDERS ====
@router.get("/work_orders/")
def get_work_orders(db: Session = Depends(get_db)):
    return db.query(WorkOrder).all()

"""@router.get("/work_orders/")
def list_work_orders(db: Session = Depends(get_db)):
    return db.query(WorkOrder).all()"""

# ==== МАРШРУТЫ ДЛЯ WORK CARDS ====
@router.get("/work_cards/{order_id}")
def get_work_cards(order_id: int, db: Session = Depends(get_db)):
    cards = db.query(WorkCard).filter(WorkCard.work_order_id == order_id).all()
    return [
        {
            "id": c.id,
            "name": c.name,
            "description": c.description
        } for c in cards
    ]

"""@router.get("/work_cards/{order_id}")
def list_work_cards(order_id: int, db: Session = Depends(get_db)):
    cards = db.query(WorkCard).filter(WorkCard.work_order_id == order_id).all()
    return cards"""

# ==== МАРШРУТЫ ДЛЯ OPERATION DESCRIPTIONS ====
@router.get("/operation_descriptions/{card_id}")
def get_operation_descriptions(card_id: int, db: Session = Depends(get_db)):
    operations = db.query(OperationDescription).filter(OperationDescription.work_card_id == card_id).all()
    return [
        {
            "id": o.id,
            "operation_number": o.operation_number,
            "description": o.description
        } for o in operations
    ]

"""@router.get("/operation_descriptions/{card_id}")
def list_operations(card_id: int, db: Session = Depends(get_db)):
    ops = db.query(OperationDescription).filter(
        OperationDescription.work_card_id == card_id
    ).all()
    return ops"""

# ==== МАРШРУТЫ ДЛЯ WORK TIMES ====
@router.get("/work_times/{operation_id}")
def get_work_times(operation_id: int, db: Session = Depends(get_db)):
    times = db.query(WorkTime).filter(WorkTime.operation_description_id == operation_id).all()
    return [
        {
            "id": t.id,
            "user_id": t.user_id,
            "start_time": t.start_time,
            "end_time": t.end_time,
            "duration": t.duration
        } for t in times
    ]

"""@router.get("/work_times/{operation_id}")
def list_work_times(operation_id: int, db: Session = Depends(get_db)):
    times = db.query(WorkTime).filter(
        WorkTime.operation_description_id == operation_id
    ).all()
    return times"""
