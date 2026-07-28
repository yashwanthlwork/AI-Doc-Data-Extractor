from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.Configuration.DBConfig import engine

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)