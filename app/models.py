from sqlalchemy import (
    Column, Integer, String, Text, DateTime,
    Enum, ForeignKey, DECIMAL
)
from sqlalchemy.orm import relationship
from app.database import Base
import enum, datetime
# arai admin
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Date, Enum, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()



# ─── Роль пользователя ────────────────────────────────────────────────
class UserRole(enum.Enum):
    admin     = 'admin'
    worker    = 'worker'
    inspector = 'inspector'

# ─── Пользователи ──────────────────────────────────────────────────────
class User(Base):
    __tablename__ = 'users'

    id           = Column(Integer, primary_key=True, index=True)
    name         = Column(String(100), nullable=False)
    role         = Column(Enum(UserRole), nullable=False)
    login        = Column(String(100), unique=True, nullable=False)
    password     = Column(String(100), nullable=False)
    uid          = Column(String(50), nullable=False)
    job_title    = Column(String(100), nullable=False)
    created_time = Column(DateTime, default=datetime.utcnow)

    # связи
    work_orders = relationship("WorkOrder", back_populates="user")
    work_cards        = relationship("WorkCard", back_populates="user")
    operations        = relationship("OperationDescription", back_populates="user")
    work_times        = relationship("WorkTime", back_populates="user")

# ─── Наряды (WorkOrder) ─────────────────────────────────────────────────
class WorkOrder(Base):
    __tablename__ = "work_orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))  # предполагаем, что есть таблица users
    created_at = Column(DateTime, default=datetime.utcnow)

    work_number = Column(String, nullable=False)
    work_date = Column(Date, nullable=False)
    work_revision = Column(String, nullable=False)
    work_order_number = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    prepared_by = Column(String, nullable=False)
    quote_number = Column(String, nullable=False)
    customer = Column(String, nullable=False)
    ordered_by = Column(String, nullable=False)
    customer_po_number = Column(String, nullable=False)
    rig_number = Column(String, nullable=False)
    well_number = Column(String, nullable=False)
    q_ty = Column(Integer, nullable=False)
    unit = Column(String, nullable=False)
    description = Column(String, nullable=False)
    serial_number = Column(String, nullable=False)
    job_description = Column(String, nullable=False)
    job_number = Column(String, nullable=False)
    job_date = Column(Date, nullable=False)
    job_revision = Column(String, nullable=False)
    grease_number = Column(String, nullable=False)
    protector_number = Column(String, nullable=False)
    request_number = Column(String, nullable=False)

    # связи
    user             = relationship("User", back_populates="work_orders")
    work_cards       = relationship("WorkCard", back_populates="work_order")

# ─── Рабочие карты (WorkCard) ────────────────────────────────────────────
class WorkCard(Base):
    __tablename__ = 'work_cards'

    

    id                        = Column(Integer, primary_key=True, index=True)
    work_order_id             = Column(Integer, ForeignKey("work_orders.id"), nullable=False)
    title                     = Column(String(255), nullable=False)
    job_description           = Column(Text)
    material                  = Column(Text)
    DRW_number                = Column(String(100))
    DRW_file_url              = Column(Text)
    cast_number               = Column(String(50))
    mill_certificate_number   = Column(String(50))
    user_id                   = Column(Integer, ForeignKey("users.id"), nullable=False)

    # связи
    work_order               = relationship("WorkOrder", back_populates="work_cards")
    user                     = relationship("User", back_populates="work_cards")
    operation_descriptions   = relationship("OperationDescription", back_populates="work_card")

# ─── Описания операций (OperationDescription) ─────────────────────────────
class OperationDescription(Base):
    __tablename__ = 'operation_descriptions'

    id                   = Column(Integer, primary_key=True, index=True)
    work_card_id         = Column(Integer, ForeignKey("work_cards.id"), nullable=False)
    operation            = Column(String(255))
    equipment            = Column(String(255))
    instruction_code     = Column(String(100))
    instruction_file_url = Column(Text)
    user_id              = Column(Integer, ForeignKey("users.id"), nullable=False)

    # связи
    work_card            = relationship("WorkCard", back_populates="operation_descriptions")
    user                 = relationship("User", back_populates="operations")
    work_times           = relationship("WorkTime", back_populates="operation_description")

# ─── Время выполнения (WorkTime) ───────────────────────────────────────────
class WorkTime(Base):
    __tablename__ = 'work_times'

    id                         = Column(Integer, primary_key=True, index=True)
    user_id                    = Column(Integer, ForeignKey("users.id"), nullable=False)
    operation_description_id   = Column(Integer, ForeignKey("operation_descriptions.id"), nullable=False)
    start_time                 = Column(DateTime, nullable=False)
    end_time                   = Column(DateTime, nullable=False)
    duration_minutes           = Column(Integer)

    # связи
    user                     = relationship("User", back_populates="work_times")
    operation_description    = relationship("OperationDescription", back_populates="work_times")


    # admin arai





