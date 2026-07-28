from app.Services.pdfrenderer import PDFRenderer
import uuid
from app.DBModels.document import Document
from app.Configuration.DBSession import SessionLocal

class DocumentService:

    def process_document(self, filename: str, pdf_bytes: bytes):
        renderer = PDFRenderer()
        pages_png = renderer.render(pdf_bytes)

        document=Document(
            total_page_number = len(pages_png),
            document_id = uuid.uuid4(),
            document_name=filename,
            process_stage = "UPLOADED",
            document_bytes=pdf_bytes,
        )
        session = SessionLocal()
        session.add(document)
        session.commit()