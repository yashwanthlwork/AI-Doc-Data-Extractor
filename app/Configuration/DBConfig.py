from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
load_dotenv()
DB_USER=os.getenv("DB_USER")
DB_PASSWORD=os.getenv("DB_PASSWORD")
DB_BASEURL=os.getenv("DB_BASEURL")
DB_NAME=os.getenv("DB_NAME")
DBConnectionString=f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}@{DB_BASEURL}/{DB_NAME}"
engine = create_engine(DBConnectionString)
DB_Connection_Status=engine.connect()
# print(f"{DB_Connection_Status}")