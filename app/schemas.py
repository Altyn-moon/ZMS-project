from pydantic import BaseModel
from typing import List, Optional
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
    job_title: str

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    name: Optional[str]
    role: Optional[str]
    login: Optional[str]
    password: Optional[str]
    uid: Optional[str]
    job_title: Optional[str]

class UserOut(UserBase):
    id: int
    created_time: datetime

    class Config:
        from_attributes = True


class WorkTimeOut(BaseModel):
    id: int
    start_time: datetime
    end_time: datetime
    duration_minutes: int

    class Config:
        from_attributes = True

class OperationDescriptionOut(BaseModel):
    id: int
    work_card_id: int
    operation: Optional[str] = None
    equipment: Optional[str] = None
    instruction_code: Optional[str]
    instruction_file_url: Optional[str]
    user_id: Optional[int] = None
    work_times: List[WorkTimeOut] = []

    class Config:
        from_attributes = True

class WorkCardOut(BaseModel):
    id: int
    work_order_id: int
    title: str
    job_description: Optional[str] = None
    material: Optional[str]
    DRW_number: Optional[str]
    DRW_file_url: Optional[str]
    cast_number: Optional[str]
    mill_certificate_number: Optional[str]
    user_id: Optional[int] = None
    operation_descriptions: List[OperationDescriptionOut] = []

    class Config:
        from_attributes = True

class WorkOrderOut(BaseModel):
    id: int
    work_order_number: str
    description: str
    customer: Optional[str]
    work_cards: List[WorkCardOut] = []

    class Config:
        from_attributes = True
