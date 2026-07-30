from app.Configuration.DBSession import SessionLocal
from app.DBModels.document_type import DocumentType
from sqlalchemy import select
from sqlalchemy.orm import Session

class DocumentTypeService:
    def create_document_type(self,document_type_name:str,document_type_description:str)-> DocumentType:
        document_type_name = document_type_name.strip().upper()
        document_type_description = document_type_description.strip()
        if not document_type_name:
            raise ValueError("Document type name cannot be empty.")
        if not document_type_description:
            raise ValueError("Document type description cannot be empty.")
        session:Session = SessionLocal()
        try:
                if self._check_document_type_exists(session, document_type_name):
                    raise ValueError("Document type already exists.")
                document_type = DocumentType(
                    document_type_name = document_type_name,
                    description = document_type_description
                )
                session.add(document_type)
                session.commit()
                session.refresh(document_type)
        except Exception:
                session.rollback()
                raise
        finally:
                session.close()
        return document_type
    
    def _check_document_type_exists(self, session:Session, document_type_name: str) -> bool:
        document_type_exists = session.scalar(
            select(DocumentType).where(
                DocumentType.document_type_name == document_type_name
            )
        )

        return document_type_exists is not None

    def get_all_document_types(self)-> list[DocumentType]:
        session:Session = SessionLocal()
        try:
            return session.scalars(
                    select(DocumentType).order_by(DocumentType.document_type_name)
            ).all()
        finally:
            session.close()

        
            
            
