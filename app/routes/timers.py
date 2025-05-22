from fastapi import APIRouter, Depends, HTTPException, Request, Body
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import pytz
from app.database import get_db
from app import models, schemas

router = APIRouter()

kz_tz = pytz.timezone("Asia/Atyrau")

@router.post("/api/start-time/")
def start_timer(operation_description_id: int, request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")

    start_time = datetime.now(kz_tz)

    work_time = models.WorkTime(
        user_id=user_id,
        operation_description_id=operation_description_id,
        start_time=start_time,
        end_time=None,
        duration_minutes=0
    )

    db.add(work_time)
    db.commit()
    db.refresh(work_time)

    return {
        "work_time_id": work_time.id,
        "start_time": start_time.isoformat()  # чтобы в JS работало без проблем
    }

"""
@router.post("/api/stop-time/")
def stop_timer(work_time_id: int, db: Session = Depends(get_db)):
    work_time = db.query(models.WorkTime).get(work_time_id)
    if not work_time:
        raise HTTPException(status_code=404, detail="WorkTime not found")

    work_time.end_time = datetime.now(kz_tz)  # С правильной временной зоной
    delta = work_time.end_time - work_time.start_time
    work_time.duration_minutes = round(delta.total_seconds() / 60, 2)

    db.commit()
    return {
        "work_time_id": work_time.id,
        "duration": work_time.duration_minutes
    }"""


@router.post("/api/stop-time/")
def stop_timer(
    work_time_id: int = Body(...),
    duration_seconds: int = Body(...),
    db: Session = Depends(get_db)
):
    work_time = db.query(models.WorkTime).get(work_time_id)
    if not work_time:
        raise HTTPException(status_code=404, detail="WorkTime not found")

    now = datetime.now(kz_tz)
    work_time.end_time = now
    work_time.duration_minutes = round(duration_seconds / 60, 2)

    db.commit()

    return {
        "work_time_id": work_time.id,
        "duration": work_time.duration_minutes
    }


@router.get("/api/active-timer/")
def get_active_timer(request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")

    wt = (
        db.query(models.WorkTime)
        .filter(models.WorkTime.user_id == user_id, models.WorkTime.end_time == None)
        .order_by(models.WorkTime.start_time.desc())
        .first()
    )

    if not wt:
        return {"active": False}

    return {
        "active": True,
        "work_time_id": wt.id,
        "start_time": wt.start_time.isoformat(),
        "operation_description_id": wt.operation_description_id,
        "order_id": wt.operation_description.work_card.work_order.id,
        "card_id": wt.operation_description.work_card.id,
    }
"""
@router.post("/save-time/")
def save_time(data: dict, db: Session = Depends(get_db)):
    op_id = data.get("operation_id")
    user_id = data.get("user_id")
    duration_str = data.get("duration")  # формат '00:01:25'

    h, m, s = map(int, duration_str.split(":"))
    duration_minutes = round(h * 60 + m + s / 60, 2)
    duration_seconds = h * 3600 + m * 60 + s

    now = datetime.now(kz_tz)
    new_time = models.WorkTime(
        user_id=user_id,
        operation_description_id=op_id,
        start_time=now,
        end_time=now + timedelta(seconds=duration_seconds),
        duration_minutes=duration_minutes
    )

    db.add(new_time)
    db.commit()
    db.refresh(new_time)
    return {"status": "ok", "id": new_time.id}
"""
