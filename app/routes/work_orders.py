from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud, models
from app.database import get_db
from app.schemas import WorkOrderCreate, WorkOrderRead
from app.models import WorkOrder

router = APIRouter()
# сохранения только WorkOrder
#@router.post("/workorders", response_model=WorkOrderRead)
#def create_work_order(work_order: WorkOrderCreate, db: Session = Depends(get_db)):
    #db_work_order = WorkOrder(**work_order.dict())
    #db.add(db_work_order)
    #db.commit()
    #db.refresh(db_work_order)
    #return db_work_order

@router.post("/api/full-workorder")
def create_full_workorder(data: schemas.FullWorkOrder, db: Session = Depends(get_db)):
    try:
        # 1. Создаём заказ
        work_order = models.WorkOrder(**data.work_order.dict())
        db.add(work_order)
        db.commit()
        db.refresh(work_order)

        # 2. Создаём карточку
        work_card_data = data.work_card.dict()
        work_card_data["work_order_id"] = work_order.id
        work_card = models.WorkCard(**work_card_data)
        db.add(work_card)
        db.commit()
        db.refresh(work_card)

        # 3. Создаём операции
        for op in data.operations:
            db_op = models.OperationDescription(
                work_card_id=work_card.id,
                **op.dict()
            )
            db.add(db_op)

        db.commit()
        return {"message": "Всё успешно сохранено"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))