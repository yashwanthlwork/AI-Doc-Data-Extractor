from datetime import datetime
from sqlalchemy import Uuid,Text,LargeBinary,DateTime,func,Integer,ForeignKey,JSON
from sqlalchemy.orm import Mapped,mapped_column
from uuid import UUID,uuid4
from app.DBModels.base import Base
from typing import Any

class Document(Base):
    __tablename__="Documents"

    document_id: Mapped[UUID] = mapped_column(Uuid,primary_key=True,default=uuid4)
    document_name: Mapped[str] = mapped_column(Text)
    total_page_number: Mapped[int] = mapped_column(Integer)
    create_date: Mapped[datetime] = mapped_column(DateTime,server_default=func.now())
    update_date: Mapped[datetime] = mapped_column(DateTime,server_default=func.now(),onupdate=func.now())
    process_stage: Mapped[str] = mapped_column(Text)
    document_bytes: Mapped[bytes] = mapped_column(LargeBinary)
    document_hash: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    document_type_id: Mapped[UUID | None] = mapped_column(Uuid,ForeignKey("DocumentTypes.document_type_id"),nullable=True)
    extracted_data: Mapped[list[dict[str, Any]]] = mapped_column(JSON,nullable=True)


