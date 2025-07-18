from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.models import Document, WorkCard
from app.dependencies import get_db

router = APIRouter()

@router.post("/documents/upload")
def upload_document(
    work_card_id: int = Form(...),
    type: str = Form(...),
    number: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    if type not in ('Certificate', 'DRW', 'Instruction'):
        raise HTTPException(status_code=400, detail="Invalid document type")

    content = file.file.read()
    url = f"/static/uploads/{file.filename}"

    doc = Document(
        work_card_id=work_card_id,
        type=type,
        number=number,
        pdf_file=content,
        url=url,
        created_at=datetime.utcnow()
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)

    return {"status": "success", "document_id": doc.id}

@router.get("/documents/{doc_id}")
def get_document(doc_id: int, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    return {
        "id": doc.id,
        "type": doc.type,
        "number": doc.number,
        "url": doc.url,
        "created_at": doc.created_at
    }

 #arai admin
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/documents/upload")
async def upload_document(file: UploadFile = File(...)):
    # Пример простой обработки
    contents = await file.read()
    filename = file.filename

    # Здесь можно сохранить в БД или на диск
    print(f"✅ Загружен файл: {filename}, размер: {len(contents)} байт")

    return JSONResponse(content={"filename": filename, "status": "ok"})
