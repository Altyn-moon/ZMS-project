"""from fastapi import APIRouter

router = APIRouter()

@router.get("/users")
def get_users():
    return {"message": "Users endpoint working!"}"""

# app/routes/users.py
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from typing import List
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.dependencies import get_db
from app.models import User
#from app.database import get_db
from app.dependencies import get_current_user
from app import crud, schemas

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.post("/", response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)

@router.get("/{user_id}", response_model=schemas.UserOut)
def read_user(user_id: int, db: Session = Depends(get_db)):
    return crud.get_user(db=db, user_id=user_id)

@router.get("/", response_model=List[schemas.UserOut])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_users(db=db, skip=skip, limit=limit)

@router.put("/{user_id}", response_model=schemas.UserOut)
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    updated = crud.update_user(db, user_id, user)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return updated

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_user(db, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}

@router.get("/dashboard", response_class=HTMLResponse)
def get_dashboard(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user_name = current_user.name
    work_items = db.query(WorkOrder).filter(WorkOrder.user_id == current_user.id).all()  # или подбери свою логику фильтра
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "user_name": user_name,
        "work_items": work_items
    })


