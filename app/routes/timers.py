from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime, timedelta

from app.dependencies import get_db
from app.models import WorkTime

router = APIRouter()

# === Модель входных данных ===
class TimeEntry(BaseModel):
    user_id: int
    operation_description_id: int
    duration: str  # формат HH:MM:SS

# === Сохранение времени выполнения ===
@router.post("/save-time/")
def save_time(entry: TimeEntry, db: Session = Depends(get_db)):
    try:
        # Преобразуем duration из строки в часы, минуты, секунды
        hours, minutes, seconds = map(int, entry.duration.split(":"))
        duration_minutes = hours * 60 + minutes + seconds // 60

        now = datetime.now()
        end_time = now
        start_time = end_time - timedelta(minutes=duration_minutes)

        new_time = WorkTime(
            user_id=entry.user_id,
            operation_description_id=entry.operation_description_id,
            start_time=start_time,
            end_time=end_time,
            duration_minutes=duration_minutes
        )
        db.add(new_time)
        db.commit()
        db.refresh(new_time)

        return {"message": "Время успешно сохранено", "id": new_time.id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
