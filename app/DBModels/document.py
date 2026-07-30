from datetime import datetime
from sqlalchemy import Uuid,Text,LargeBinary,DateTime,func,Integer,ForeignKey
from sqlalchemy.orm import Mapped,mapped_column
import uuid
from app.DBModels.base import Base

class Document(Base):
    __tablename__="Documents"

    document_id: Mapped[uuid.UUID] = mapped_column(Uuid,primary_key=True)
    document_name: Mapped[str] = mapped_column(Text)
    total_page_number: Mapped[int] = mapped_column(Integer)
    create_date: Mapped[datetime] = mapped_column(DateTime,server_default=func.now())
    update_date: Mapped[datetime] = mapped_column(DateTime,server_default=func.now(),onupdate=func.now())
    process_stage: Mapped[str] = mapped_column(Text)
    document_bytes: Mapped[bytes] = mapped_column(LargeBinary)
    document_type_id: Mapped[uuid.UUID | None] = mapped_column(
    Uuid,
    ForeignKey("DocumentTypes.document_type_id"),
    nullable=True
)


