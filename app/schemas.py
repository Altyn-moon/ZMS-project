# from pydantic import BaseModel
# from typing import Optional
# from datetime import datetime

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

# class UserCreate(UserBase):
#    pass

# class UserUpdate(BaseModel):
#    name: Optional[str]
#    role: Optional[str]
#    login: Optional[str]
#   password: Optional[str]
#    uid: Optional[str]
#    job_title: Optional[str]

# class UserOut(UserBase):
#    id: int
#    created_time: datetime

class Config:
    from_attributes = True

