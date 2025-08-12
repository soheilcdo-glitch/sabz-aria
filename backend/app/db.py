from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DATABASE_URL = "mysql+pymysql://root:@localhost:3306/dashboard_db"

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()



DATABASE_URL = "mysql+pymysql://root:@localhost:3306/dashboard_db"