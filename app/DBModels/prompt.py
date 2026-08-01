from app.DBModels.base import Base
from sqlalchemy import Text,func,ForeignKey,Uuid,DateTime
from sqlalchemy.orm import Mapped,mapped_column
from uuid import UUID,uuid4
from datetime import datetime

class Prompt(Base):
    __tablename__="Prompts"

    prompt_id:Mapped[UUID] = mapped_column(Uuid,primary_key=True,default=uuid4)
    prompt_name: Mapped[str] = mapped_column(Text,unique=True,nullable=False)    
    document_type_id:Mapped[UUID] = mapped_column(Uuid,ForeignKey("DocumentTypes.document_type_id"),unique=True,nullable=False)
    prompt:Mapped[str] = mapped_column(Text,nullable=False)
    create_date:Mapped[datetime] = mapped_column(DateTime,server_default=func.now(),nullable=False)
    update_date:Mapped[datetime] = mapped_column(DateTime,server_default=func.now(),onupdate=func.now(),nullable=False)