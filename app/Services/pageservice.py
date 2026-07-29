from app.Configuration.DBSession import SessionLocal
from sqlalchemy import select
from app.DBModels.document import Document
from app.DBModels.page import Page
from app.Services.pdfrenderer import PDFRenderer

class PageService:

    def upload_pages(self, document_id):
        session = SessionLocal()

        try:
            document = session.scalar(
                select(Document).where(Document.document_id == document_id)
            )
            renderer=PDFRenderer()
            pages_png=renderer.render(document.document_bytes)
            for page_number, page_png in enumerate(pages_png, start=1):
                page = Page(
                    document_id=document.document_id,
                    page_number=page_number,
                    page_png=page_png,
                    page_markdown="",
                    process_stage="UPLOADED",
                    )
                session.add(page)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
            