from app.Configuration.DBSession import SessionLocal
from sqlalchemy import select
from app.DBModels.document import Document
from app.DBModels.page import Page
from app.Services.ollamaservice import OllamaService
import pymupdf

class PageService:

    def upload_pages(self, document_id):
        session = SessionLocal()

        try:
            document = session.scalar(
                select(Document).where(Document.document_id == document_id)
            )

            if document is None:
                raise ValueError("Document not found")


            pdf = pymupdf.open(stream=document.document_bytes, filetype="pdf")

            try:
                png_pages = []

                for page in pdf:
                    pixmap = page.get_pixmap()
                    png_pages.append(pixmap.tobytes("png"))

            finally:
                pdf.close()

            document.total_page_number = len(png_pages)
            for page_number, page_png in enumerate(png_pages, start=1):
                page = Page(
                    document_id=document.document_id,
                    page_number=page_number,
                    page_png=page_png,
                    page_markdown="",
                    process_stage="UPLOADED",
                    )
                session.add(page)
            document.process_stage = "PAGES_CREATED"
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
            

    def extract_markdown(self, document_id):
        session = SessionLocal()

        try:
            ollama_service = OllamaService()
            document = session.scalar(
                select(Document).where(Document.document_id == document_id)
            )

            pages = session.scalars(
                select(Page)
                .where(Page.document_id == document_id)
                .order_by(Page.page_number)
            ).all()

            if not pages:
                raise ValueError("No pages found for this document")

            for page in pages:
                markdown = ollama_service.extract_markdown(page.page_png)
                page.page_markdown=markdown
                page.process_stage = "MARKDOWN_EXTRACTED"
            document.process_stage = "MARKDOWN_EXTRACTED"
            session.commit()

        except:
            session.rollback()
            raise

        finally:
            session.close()
            