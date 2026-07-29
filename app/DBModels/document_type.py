from app.DBModels.base import Base
from sqlalchemy import Text, DateTime, func,Uuid,text
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
import uuid

class DocumentType(Base):
    __tablename__="DocumentTypes"

    document_type_id: Mapped[uuid.UUID] = mapped_column(
    Uuid,
    primary_key=True,
    server_default=text("gen_random_uuid()"))
    document_type_name:Mapped[str]=mapped_column(Text,unique=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    create_date: Mapped[datetime] = mapped_column(DateTime,server_default=func.now())
    update_date: Mapped[datetime] = mapped_column(DateTime,server_default=func.now(),onupdate=func.now())



