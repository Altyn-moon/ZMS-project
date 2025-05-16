from sqlalchemy.orm import Session
from app import models, schemas
from app.models import WorkOrder, WorkCard, OperationDescription, WorkTime

def get_work_orders(db: Session, skip: int=0, limit: int=100):
    return db.query(WorkOrder).offset(skip).limit(limit).all()

def get_work_cards_by_order(db: Session, order_id: int):
    return db.query(WorkCard)\
             .filter(WorkCard.work_order_id == order_id)\
             .all()

def get_operations_by_card(db: Session, card_id: int):
    return db.query(OperationDescription)\
             .filter(OperationDescription.work_card_id == card_id)\
             .all()