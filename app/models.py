from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String)  # например: 'user', 'admin', 'inspector'
    name = Column(String, unique=True, index=True)
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id       = Column(Integer, primary_key=True, index=True)
    login    = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String(100), nullable=False)
    role     = Column(String(50),  nullable=False)  # 'user', 'admin', 'inspector'
    name     = Column(String(100), unique=True, index=True, nullable=False)
    uid      = Column(String(50),  unique=True, nullable=True)

    work_times = relationship("WorkTime", back_populates="user")
    # если понадобится, можно добавить back_populates у WorkOrder.author, OperationDescription.responsible

class WorkOrder(Base):
    __tablename__ = "work_orders"

    id                = Column(Integer, primary_key=True)
    code              = Column(String(50),  nullable=False, index=True)
    name              = Column(String(255), nullable=False)
    author_id         = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    created_at        = Column(DateTime, server_default=func.now(), nullable=False)
    zms_code          = Column(String(100))
    grease_number     = Column(String(50))
    protector_number  = Column(String(50))
    application_number= Column(String(50))
    work_order_number = Column(String(50))
    customer          = Column(String(255))
    unit              = Column(String(50))
    quantity          = Column(DECIMAL(10,2))

    author     = relationship("User")
    work_cards = relationship("WorkCard", back_populates="order")

class WorkCard(Base):
    __tablename__ = "work_cards"

    id                   = Column(Integer, primary_key=True)
    work_order_id        = Column(Integer, ForeignKey("work_orders.id"), nullable=False, index=True)
    name                 = Column(String(255), nullable=False)
    description          = Column(Text)
    material             = Column(Text)
    drawing_number       = Column(String(100))
    drawing_file_url     = Column(Text)
    melt_number          = Column(String(50))
    certificate_number   = Column(String(50))

    order      = relationship("WorkOrder", back_populates="work_cards")
    operations = relationship("OperationDescription", back_populates="card")

class OperationDescription(Base):
    __tablename__ = "operation_descriptions"

    id                    = Column(Integer, primary_key=True)
    work_card_id          = Column(Integer, ForeignKey("work_cards.id"), nullable=False, index=True)
    operation             = Column(String(255))
    equipment             = Column(String(255))
    instruction_code      = Column(String(100))
    instruction_file_url  = Column(Text)
    responsible_user_id   = Column(Integer, ForeignKey("users.id"), index=True)

    card        = relationship("WorkCard", back_populates="operations")
    responsible = relationship("User")
    work_times  = relationship("WorkTime", back_populates="operation")

class WorkTime(Base):
    __tablename__ = "work_times"

    id                         = Column(Integer, primary_key=True)
    user_id                    = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    operation_description_id   = Column(Integer, ForeignKey("operation_descriptions.id"), nullable=False, index=True)
    start_time                 = Column(DateTime, nullable=False)
    end_time                   = Column(DateTime, nullable=False)
    duration_minutes           = Column(Integer)  # при необходимости считаем в приложении

    user      = relationship("User", back_populates="work_times")
    operation = relationship("OperationDescription", back_populates="work_times")"""


