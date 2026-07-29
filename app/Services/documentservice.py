from app.Services.pdfrenderer import PDFRenderer
from app.Services.pageservice import PageService
import uuid
from app.DBModels.document import Document
from app.Configuration.DBSession import SessionLocal

class DocumentService:

    def upload_document(self, filename: str, pdf_bytes: bytes):
        session = SessionLocal()
        try:
            renderer = PDFRenderer()
            pages_png = renderer.render(pdf_bytes)

            document=Document(
                total_page_number = len(pages_png),
                document_id = uuid.uuid4(),
                document_name=filename,
                process_stage = "UPLOADED",
                document_bytes=pdf_bytes,
            )
            session.add(document)
            session.commit()
            page_service = PageService()
            page_service.upload_pages(document.document_id)
        except:
            session.rollback()
            raise
        finally:
            session.close()
            