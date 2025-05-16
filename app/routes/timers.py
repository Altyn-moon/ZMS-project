from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import WorkTime
from datetime import datetime, timedelta

router = APIRouter()

class TimeEntry(BaseModel):
    operation_id: int
    user_id: int
    duration: str  # формат 'HH:MM:SS'

@router.post("/save-time/")
def save_time(entry: TimeEntry, db: Session = Depends(get_db)):
    hours, minutes, seconds = map(int, entry.duration.split(":"))
    start_time = datetime.now()
    end_time = start_time + timedelta(hours=hours, minutes=minutes, seconds=seconds)
    duration_minutes = hours * 60 + minutes + seconds // 60

    db_entry = WorkTime(
        operation_description_id=entry.operation_id,
        user_id=entry.user_id,
        start_time=start_time,
        end_time=end_time,
        duration_minutes=duration_minutes
    )
    db.add(db_entry)
    db.commit()
    return {"status": "saved"}
