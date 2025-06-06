from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from datetime import datetime, date
from typing import Literal

# ─── Аутентификация ─────────────────────────────
class AdminLogin(BaseModel):
    name: str
    password: str

# ─── Пользователь ─────────────────────────────
class UserBase(BaseModel):
    name: str
    role: str
    login: str
    password: str
    uid: str

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    name: Optional[str]
    role: Optional[str]
    login: Optional[str]
    password: Optional[str]
    uid: Optional[str]

class UserOut(UserBase):
    id: int
    job_title: str
    created_time: datetime

    class Config:
        from_attributes = True

# ─── Документ ─────────────────────────────
class DocumentOut(BaseModel):
    id: int
    work_card_id: Optional[int]
    type: str
    number: Optional[str]
    url: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

# ─── Таймер ─────────────────────────────
class WorkTimeBase(BaseModel):
    operation_description_id: int

class WorkTimeCreate(WorkTimeBase):
    start_time: datetime
    end_time: datetime
    duration_minutes: int

class WorkTimeOut(WorkTimeBase):
    id: int
    start_time: datetime
    end_time: datetime
    duration_minutes: int

    class Config:
        from_attributes = True

# ─── Описание операций ─────────────────────────────
class OperationDescriptionBase(BaseModel):
    work_card_id: int
    operation: Optional[str] = None
    equipment: Optional[str] = None
    user_id: Optional[int] = None
    documents_id: Optional[int] = None

class OperationDescriptionCreate(OperationDescriptionBase):
    pass

class OperationDescriptionOut(OperationDescriptionBase):
    id: int
    work_times: List[WorkTimeOut] = []

    class Config:
        from_attributes = True

# ─── Рабочие карты ─────────────────────────────
class WorkCardBase(BaseModel):
    work_order_id: int
    title: str
    material: Optional[str] = None
    cast_number: Optional[str] = None
    user_id: Optional[int] = None
    documents_id: Optional[int] = None

class WorkCardCreate(WorkCardBase):
    pass

class WorkCardOut(WorkCardBase):
    id: int
    operation_descriptions: List[OperationDescriptionOut] = []

    class Config:
        from_attributes = True

# ─── Наряды (WorkOrders) ─────────────────────────────
class WorkOrderBase(BaseModel):
    work_number: str
    work_date: date
    work_revision: str
    work_order_number: str
    start_date: date
    end_date: date
    prepared_by: str
    quote_number: str
    customer: str
    ordered_by: str
    customer_po_number: str
    rig_number: str
    well_number: str
    q_ty: int
    unit: str
    description: str
    serial_number: str
    job_description: str
    job_number: str
    job_date: date
    job_revision: str
    grease_number: str
    protector_number: str
    request_number: str
    


class WorkOrderCreate(WorkOrderBase):
    user_id: Optional[int] = None

class WorkOrderRead(WorkOrderBase):
    id: int
    user_id: Optional[int] = None
    created_at: datetime

    class Config:
        orm_mode = True

from pydantic import BaseModel
from typing import Optional
from datetime import date

class WorkOrderOut(BaseModel):
    id: int
    work_order_number: str
    description: str
    customer: Optional[str]
    work_cards: List[WorkCardOut] = []

    class Config:
        orm_mode = True  # чтобы FastAPI мог конвертировать из ORM-модели SQLAlchemy



from typing import List

class FullWorkOrder(BaseModel):
    work_order: WorkOrderCreate
    work_card: WorkCardCreate
    operations: List[OperationDescriptionCreate]


class WorkCardCreate(BaseModel):
    title: Optional[str]
    material: Optional[str]
    cast_number: Optional[str]
    
class DocumentCreate(BaseModel):
    work_card_id: Optional[int]
    operation_description_id: Optional[int]
    type: str  # должен быть 'Certificate', 'DRW' или 'Instruction'
    number: Optional[str]
    url: Optional[str]  # если файл загружается и путь сохраняется
    
class DocumentIn(BaseModel):
    type: Literal['DRW', 'Certificate', 'Instruction']
    number: Optional[str]
    url: Optional[str]
    work_card_id: Optional[int]
    operation_description_id: Optional[int]

class OperationIn(BaseModel):
    operation: str
    equipment: Optional[str]
    user_id: int
    documents: Optional[list[DocumentIn]]

class WorkCardIn(BaseModel):
    title: str
    material: Optional[str]
    cast_number: Optional[str]
    user_id: int
    operations: List[OperationIn]

class WorkOrderIn(BaseModel):
    work_number: str
    work_date: date
    work_revision: str
    work_order_number: str
    start_date: date
    end_date: date
    prepared_by: str
    quote_number: str
    customer: str
    ordered_by: str
    customer_po_number: str
    rig_number: str
    well_number: str
    q_ty: str
    unit: str
    description: str
    serial_number: str
    job_description: str
    job_number: str
    job_date: date
    job_revision: str
    grease_number: str
    protector_number: str
    request_number: str
    user_id: int
    work_cards: List[WorkCardIn]

class FullWorkOrder(BaseModel):

    work_order: WorkOrderIn


