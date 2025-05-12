from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app import models

router = APIRouter()

"""
@router.get("/check_uid/{uid}")
def check_uid(uid: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.card_uid == uid).first()
    if user:
        return {"message": f"Добро пожаловать, {user.name}!"}
    else:
        return {"message": "Карта не зарегистрирована."} """

@router.get("/check_uid/{uid}")
def check_uid(uid: str):
    return {"message": "Проверка UID пока отключена (без базы данных)."}

