from sqlalchemy import (
    Column, Integer, String, Text, DateTime, Date,
    Enum, ForeignKey
)
from sqlalchemy.orm import relationship
from app.database import Base
import enum, datetime

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
    created_time = Column(DateTime, default=datetime.datetime.utcnow)

    # связи
    work_orders       = relationship("WorkOrder", back_populates="user")
    work_cards        = relationship("WorkCard", back_populates="user")
    operations        = relationship("OperationDescription", back_populates="user")
    work_times        = relationship("WorkTime", back_populates="user")

# ─── Наряды (WorkOrder) ─────────────────────────────────────────────────
class WorkOrder(Base):
    __tablename__ = "work_orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime)
    work_number = Column(String(100))
    work_date = Column(Date)
    work_revision = Column(String(50))
    work_order_number = Column(String(100))
    start_date = Column(Date)
    end_date = Column(Date)
    prepared_by = Column(String(100))
    quote_number = Column(String(200))
    customer = Column(String(255))
    ordered_by = Column(String(100))
    customer_po_number = Column(String(100))
    rig_number = Column(String(100))
    well_number = Column(String(100))
    q_ty = Column(String(50))
    unit = Column(String(50))
    description = Column(String(200))
    serial_number = Column(String(100))
    job_description = Column(Text)
    job_number = Column(String(100))
    job_date = Column(Date)
    job_revision = Column(String(50))
    grease_number = Column(String(100))
    protector_number = Column(String(100))
    request_number = Column(String(100))

    # связи
    user = relationship("User", back_populates="work_orders")
    work_cards = relationship("WorkCard", back_populates="work_order")

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
    __tablename__ = "work_times"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    operation_description_id = Column(Integer, ForeignKey("operation_descriptions.id"))
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    duration_minutes = Column(Integer)

    # связи
    user                     = relationship("User", back_populates="work_times")
    operation_description    = relationship("OperationDescription", back_populates="work_times")
