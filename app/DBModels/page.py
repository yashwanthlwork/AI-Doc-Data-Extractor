from sqlalchemy.orm import Mapped,mapped_column
import uuid
from sqlalchemy import Uuid, LargeBinary, Text, DateTime, func,Integer,ForeignKey
from datetime import datetime
from app.DBModels.base import Base

class Page(Base):
    __tablename__="Pages"

    document_id: Mapped[uuid.UUID] = mapped_column(Uuid,ForeignKey("Documents.document_id"),primary_key=True)
    page_number: Mapped[int] = mapped_column(Integer,primary_key=True)
    create_date: Mapped[datetime] = mapped_column(DateTime,server_default=func.now())
    update_date: Mapped[datetime] = mapped_column(DateTime,server_default=func.now(), onupdate=func.now())
    page_png: Mapped[bytes] = mapped_column(LargeBinary)
    page_markdown: Mapped[str] = mapped_column(Text)
    process_stage: Mapped[str] = mapped_column(Text)



