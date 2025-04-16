# models.py

from sqlalchemy import Column, Integer, String
from app.database import Base

class User(Base):
    __tablename__ = "users"  # Название таблицы в MySQL

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    card_uid = Column(String(100), unique=True, index=True)
