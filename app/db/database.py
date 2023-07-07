from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from app.credentials import DATABASE_URI

engine = create_engine(DATABASE_URI)
SessionLocal = sessionmaker(engine, expire_on_commit=False, class_=Session)

Base = declarative_base()
