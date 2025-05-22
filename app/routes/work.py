from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db
#from app.models import WorkOrder, WorkCard, OperationDescription, WorkTime
from app.schemas import WorkOrderOut, WorkCardOut, OperationDescriptionOut
from app import crud
from app.models import WorkTime

router = APIRouter(prefix="/api")
#router = APIRouter(tags=["work"])

# ==== МАРШРУТЫ ДЛЯ WORK ORDERS ====
@router.get("/work_orders", response_model=list[WorkOrderOut])
def read_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_work_orders(db, skip, limit)

# ==== МАРШРУТЫ ДЛЯ WORK CARDS ====
@router.get("/work_cards/{order_id}", response_model=list[WorkCardOut])
def read_cards(order_id: int, db: Session = Depends(get_db)):
    cards = crud.get_work_cards_by_order(db, order_id)
    if cards is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return cards

# ==== МАРШРУТЫ ДЛЯ OPERATION DESCRIPTIONS ====
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db
#from app.models import WorkOrder, WorkCard, OperationDescription, WorkTime
from app.schemas import WorkOrderOut, WorkCardOut, OperationDescriptionOut
from app import crud

router = APIRouter(prefix="/api")
#router = APIRouter(tags=["work"])

# ==== МАРШРУТЫ ДЛЯ WORK ORDERS ====
@router.get("/work_orders", response_model=list[WorkOrderOut])
def read_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_work_orders(db, skip, limit)

# ==== МАРШРУТЫ ДЛЯ WORK CARDS ====
@router.get("/work_cards/{order_id}", response_model=list[WorkCardOut])
def read_cards(order_id: int, db: Session = Depends(get_db)):
    cards = crud.get_work_cards_by_order(db, order_id)
    if cards is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return cards

# ==== МАРШРУТЫ ДЛЯ OPERATION DESCRIPTIONS ====
@router.get("/operations/{card_id}", response_model=list[OperationDescriptionOut])
def read_operations(card_id: int, db: Session = Depends(get_db)):
    ops = crud.get_operations_by_card(db, card_id)
    if ops is None:
        raise HTTPException(status_code=404, detail="Card not found")
    return ops

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

@router.get("/operations/{card_id}", response_model=list[OperationDescriptionOut])
def read_operations(card_id: int, db: Session = Depends(get_db)):
    ops = crud.get_operations_by_card(db, card_id)
    if ops is None:
        raise HTTPException(status_code=404, detail="Card not found")
    return ops

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

