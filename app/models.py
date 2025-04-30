# """from sqlalchemy import Column, Integer, String
# from sqlalchemy.ext.declarative import declarative_base

# Base = declarative_base()

# class User(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True, index=True)
#     login = Column(String, unique=True, index=True)
#     password = Column(String)
#     role = Column(String)  # например: 'user', 'admin', 'inspector'
#     name = Column(String, unique=True, index=True)
# """

# # app/models.py
# from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, ForeignKey, DECIMAL
# from sqlalchemy.orm import relationship
# from sqlalchemy.sql import func
# from app.database import Base
# import enum
# import datetime

# class UserRole(enum.Enum):
#     admin = 'admin'
#     worker = 'worker'
#     inspector = 'inspector'

# class User(Base):
#     __tablename__ = 'users'

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(100))
#     role = Column(Enum(UserRole))
#     login = Column(String(100), unique=True)
#     password = Column(String(100))
#     uid = Column(String(50))
#     job_title = Column(String(100))
#     created_time = Column(DateTime, default=datetime.datetime.utcnow)

#     # work_times = relationship("WorkTime", back_populates="user", foreign_keys="WorkTime.user_id")
#     # created_orders = relationship("WorkOrder", back_populates="creator", foreign_keys="WorkOrder.users_id")
#     # created_cards = relationship("WorkCard", back_populates="creator", foreign_keys="WorkCard.users_id")
#     # created_operations = relationship("OperationDescription", back_populates="creator", foreign_keys="OperationDescription.users_id")
#     # created_work_times = relationship("WorkTime", back_populates="creator", foreign_keys="WorkTime.users_id")

# class WorkOrder(Base):
#     __tablename__ = "work_orders"

#     id = Column(Integer, primary_key=True)
#     code = Column(String(50), nullable=False, index=True)
#     name = Column(String(255), nullable=False)
#     author_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
#     created_at = Column(DateTime, server_default=func.now(), nullable=False)
#     zms_code = Column(String(100))
#     grease_number = Column(String(50))
#     protector_number = Column(String(50))
#     application_number = Column(String(50))
#     work_order_number = Column(String(50))
#     customer = Column(String(255))
#     unit = Column(String(50))
#     quantity = Column(DECIMAL(10,2))
#     users_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

#     # author = relationship("User", foreign_keys=[author_id])
#     # creator = relationship("User", back_populates="created_orders", foreign_keys=[users_id])
#     # work_cards = relationship("WorkCard", back_populates="order")

# class WorkCard(Base):
#     __tablename__ = "work_cards"

#     id = Column(Integer, primary_key=True)
#     work_order_id = Column(Integer, ForeignKey("work_orders.id"), nullable=False, index=True)
#     name = Column(String(255), nullable=False)
#     description = Column(Text)
#     material = Column(Text)
#     drawing_number = Column(String(100))
#     drawing_file_url = Column(Text)
#     melt_number = Column(String(50))
#     certificate_number = Column(String(50))
#     users_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

#     # order = relationship("WorkOrder", back_populates="work_cards")
#     # creator = relationship("User", back_populates="created_cards", foreign_keys=[users_id])
#     # operations = relationship("OperationDescription", back_populates="card")

# class OperationDescription(Base):
#     __tablename__ = "operation_descriptions"

#     id = Column(Integer, primary_key=True)
#     work_card_id = Column(Integer, ForeignKey("work_cards.id"), nullable=False, index=True)
#     operation = Column(String(255))
#     equipment = Column(String(255))
#     instruction_code = Column(String(100))
#     instruction_file_url = Column(Text)
#     responsible_user_id = Column(Integer, ForeignKey("users.id"), index=True)
#     users_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

#     # card = relationship("WorkCard", back_populates="operations")
#     # responsible = relationship("User", foreign_keys=[responsible_user_id])
#     # creator = relationship("User", back_populates="created_operations", foreign_keys=[users_id])
#     # work_times = relationship("WorkTime", back_populates="operation")

# class WorkTime(Base):
#     __tablename__ = "work_times"

#     id = Column(Integer, primary_key=True)
#     user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
#     operation_description_id = Column(Integer, ForeignKey("operation_descriptions.id"), nullable=False, index=True)
#     start_time = Column(DateTime, nullable=False)
#     end_time = Column(DateTime, nullable=False)
#     duration_minutes = Column(Integer)
#     users_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

#     # user = relationship("User", back_populates="work_times", foreign_keys=[user_id])
#     # creator = relationship("User", back_populates="created_work_times", foreign_keys=[users_id])
#     # operation = relationship("OperationDescription", back_populates="work_times")
