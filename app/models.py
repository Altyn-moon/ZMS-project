from sqlalchemy import (
    Column, Integer, String, Text, DateTime,
    Enum, ForeignKey, DECIMAL
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
    __tablename__ = 'work_orders'

    id               = Column(Integer, primary_key=True, index=True)
    code             = Column(String(50), nullable=False)
    name             = Column(String(255), nullable=False)
    user_id          = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at       = Column(DateTime, default=datetime.datetime.utcnow)
    zms_code         = Column(String(100))
    grease_number    = Column(String(50))
    protector_number = Column(String(50))
    request_number   = Column(String(50))
    customer         = Column(String(255))
    unit             = Column(String(50))
    quantity         = Column(DECIMAL(10, 2))

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

