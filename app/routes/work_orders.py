from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud
from app.database import get_db
from app.schemas import WorkOrderCreate, WorkOrderRead
from app.models import WorkOrder

router = APIRouter()

@router.post("/workorders", response_model=WorkOrderRead)
def create_work_order(work_order: WorkOrderCreate, db: Session = Depends(get_db)):
    db_work_order = WorkOrder(**work_order.dict())
    db.add(db_work_order)
    db.commit()
    db.refresh(db_work_order)
    return db_work_order
