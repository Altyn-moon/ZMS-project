from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AdminLogin(BaseModel):
    name: str
    password: str

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
    created_time: datetime

class Config:
    from_attributes = True

#arai admin

from pydantic import BaseModel

class UserBase(BaseModel):
    name: str
    role: str
    login: str
    password: str
    uid: str

class UserCreate(UserBase):
    pass  # или дополнительные поля для создания пользователя

from typing import Optional

class WorkCardBase(BaseModel):
    job_description: Optional[str] = None
    material: Optional[str] = None
    DRW_number: Optional[str] = None
    DRW_file_url: Optional[str] = None
    cast_number: Optional[str] = None
    mill_certificate_number: Optional[str] = None

class WorkCardCreate(WorkCardBase):
    pass  # Можно добавить дополнительные поля, если необходимо

class WorkCardOut(WorkCardBase):
    id: int

    class Config:
        orm_mode = True
class WorkCardCreate(BaseModel):
    name: Optional[str] = None
    user_id: Optional[str] = None

class WorkCard(BaseModel):
    id: int
    name: str
    user_id: int

    class Config:
        orm_mode = True


class OperationDescriptionBase(BaseModel):
    work_card_id: int
    operation: str
    equipment: Optional[str] = None
    instruction_code: Optional[str] = None
    instruction_file_url: Optional[str] = None


class OperationDescriptionCreate(OperationDescriptionBase):
    pass  # Можно добавить дополнительные поля, если необходимо

class OperationDescriptionOut(OperationDescriptionBase):
    id: int

    class Config:
        orm_mode = True

from datetime import datetime

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
        orm_mode = True
    
# schemas.py

from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime

# Базовая модель — все поля необязательны
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

# Модель для создания WorkOrder
class WorkOrderCreate(WorkOrderBase):
    user_id: Optional[int] = None
    

# Модель ответа с id
class WorkOrderRead(WorkOrderBase):
    id: int
    user_id: Optional[int] = None
    created_at: datetime  # если это поле есть в модели

    class Config:
        orm_mode = True


from pydantic import BaseModel
from typing import Optional
from datetime import date

class WorkOrderOut(BaseModel):
    id: int
    work_number: str
    work_date: date
    # и остальные поля, которые хочешь вернуть

    class Config:
        orm_mode = True  # чтобы FastAPI мог конвертировать из ORM-модели SQLAlchemy

