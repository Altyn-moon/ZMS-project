
"""from sqlalchemy.orm import Session
from app import models, schemas

# ➕ Создать пользователя
def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# 📄 Получить пользователя по ID
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

# 📄 Получить список всех пользователей
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

# ✏️ Обновить пользователя
def update_user(db: Session, user_id: int, user: schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        return None
    for var, value in vars(user).items():
        if value is not None:
            setattr(db_user, var, value)
    db.commit()
    db.refresh(db_user)
    return db_user

# ❌ Удалить пользователя
def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        return None
    db.delete(db_user)
    db.commit()
    return db_user"""

# crud.py

from sqlalchemy.orm import Session
from app import models, schemas  # Убедись, что схемы правильно импортированы

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        name=user.name,
        role=user.role,
        login=user.login,
        password=user.password,  # Лучше хэшировать пароль
        uid=user.uid,
        job_title=user.job_title
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

from app import schemas

def create_user(db: Session, user: schemas.UserCreate):
    # Логика создания пользователя

    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

# Рабочие карты
def create_work_card(db: Session, card: schemas.WorkCardCreate):
    db_card = models.WorkCard(**card.dict())
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card

def get_work_cards(db: Session, order_id: int = None, user_id: int = None, skip: int = 0, limit: int = 100):
    q = db.query(models.WorkCard)
    if order_id is not None:
        q = q.filter(models.WorkCard.work_order_id == order_id)
    if user_id is not None:
        q = q.filter(models.WorkCard.user_id == user_id)
    return q.offset(skip).limit(limit).all()

# Описания операций
def create_operation_description(db: Session, op: schemas.OperationDescriptionCreate):
    db_op = models.OperationDescription(**op.dict())
    db.add(db_op)
    db.commit()
    db.refresh(db_op)
    return db_op

def get_operation_descriptions(db: Session, card_id: int, skip: int = 0, limit: int = 100):
    return (
        db.query(models.OperationDescription)
          .filter(models.OperationDescription.work_card_id == card_id)
          .offset(skip).limit(limit)
          .all()
    )

# Записи времени
def create_work_time(db: Session, wt: schemas.WorkTimeCreate):
    db_wt = models.WorkTime(**wt.dict())
    db.add(db_wt)
    db.commit()
    db.refresh(db_wt)
    return db_wt

def get_work_times(db: Session, user_id: int = None, op_id: int = None, skip: int = 0, limit: int = 100):
    q = db.query(models.WorkTime)
    if user_id is not None:
        q = q.filter(models.WorkTime.user_id == user_id)
    if op_id is not None:
        q = q.filter(models.WorkTime.operation_description_id == op_id)
    return q.offset(skip).limit(limit).all()

# arai admin
from app import models
from app import crud

from app import schemas

def create_work_card(db: Session, card: schemas.WorkCardCreate):
    # Код для создания рабочей карты
    pass

from sqlalchemy.orm import Session
from app import models, schemas
from app.models import WorkOrder, WorkCard, OperationDescription, WorkTime


def create_work_order(db, order: schemas.WorkOrderCreate):
    db_order = models.WorkOrder(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

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

