from app.DBModels.document import Document
from app.Configuration.DBSession import SessionLocal
from app.Services.documenttypeservice import DocumentTypeService
import hashlib
from sqlalchemy.orm import Session
from sqlalchemy import select
from uuid import UUID

class DocumentService:

    def upload_document(self, filename:str, pdf_bytes: bytes):
        session = SessionLocal()
        try:
            document_hash = hashlib.sha256(pdf_bytes).hexdigest()

            existing_document = session.scalar(
                select(Document).where(
                    Document.document_hash == document_hash
                )
            )

            if existing_document:
                raise ValueError("Document already exists.")

            document=Document(
                total_page_number = 0,
                document_name=filename,
                process_stage = "UPLOADED",
                document_bytes=pdf_bytes,
                document_hash = document_hash
            )
            session.add(document)
            session.commit()
            session.refresh(document)

            return document.document_id
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    
    def update_stage(self, document_id, stage):
        session = SessionLocal()
        try:
            if not self.check_document_exists(session, document_id):
                raise ValueError("Invalid document_id")
            
            document = session.scalar(
                select(Document).where(Document.document_id == document_id)
            )
            
            document.process_stage = stage
            session.commit()
        except Exception:
            session.rollback()
            raise

        finally:
            session.close()


    def update_document_type(self,document_id:str,document_type_id:str):
        session = SessionLocal()
        try:
            if not self.check_document_exists(session, document_id):
                raise ValueError("Invalid document_id")
            
            document=session.scalar(
                select(Document).where(Document.document_id==document_id)
            )

            documenttypeservice=DocumentTypeService()

            if not documenttypeservice.check_document_type_id_exists(session, document_type_id):
                raise ValueError("Invalid document_type_id")
            
            document.document_type_id=document_type_id

            session.commit()
            session.refresh(document)
            return document
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()


    def check_document_exists(self, session:Session, document_id:UUID):
        return session.scalar(
            select(Document).where(Document.document_id == document_id)
        ) is not None
        