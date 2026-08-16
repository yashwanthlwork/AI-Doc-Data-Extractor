from sqlalchemy import create_engine
from app.Configuration.Config import (
    DB_USER,
    DB_PASSWORD,
    DB_BASEURL,
    DB_NAME
)

db_connection_string = (
    f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_BASEURL}/{DB_NAME}"
)

engine = create_engine(db_connection_string)