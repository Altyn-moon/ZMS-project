from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "mysql+mysqlconnector://root:root@localhost:3306/work_portal"

engine = create_engine(DATABASE_URL)  # ✅ Без connect_args!
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        
Base = declarative_base()

