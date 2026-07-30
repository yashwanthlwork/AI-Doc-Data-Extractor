import uuid
from app.DBModels.document import Document
from app.Configuration.DBSession import SessionLocal
from sqlalchemy import select

class DocumentService:

    def upload_document(self, filename: str, pdf_bytes: bytes):
        session = SessionLocal()
        try:
            
            document_uuid=uuid.uuid4()
            document=Document(
                total_page_number = 0,
                document_id = document_uuid,
                document_name=filename,
                process_stage = "UPLOADED",
                document_bytes=pdf_bytes,
            )
            session.add(document)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return document_uuid

    
    def update_stage(self, document_id, stage):
        session = SessionLocal()

        try:
            document = session.scalar(
                select(Document).where(Document.document_id == document_id)
            )

            document.process_stage = stage

            session.commit()

        except:
            session.rollback()
            raise

        finally:
            session.close()

    def update_document_type(self,document_id:str,document_type_id:str):
        session = SessionLocal()
        try:
            document=session.scalar(
                select(Document).where(Document.document_id==document_id)
            )
            document.document_type_id=document_type_id
            session.commit()
            session.refresh()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
        return document

            