from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.Configuration.DBSession import SessionLocal
from app.DBModels.document import Document
from app.DBModels.page import Page
from app.Services.promptservice import PromptService
from app.Services.ollamaservice import OllamaService
from app.Services.pageservice import PageService
from app.DBModels.prompt import Prompt


class DocumentDataExtractionService:

    def extract_data(self, document_id: UUID):

        session: Session = SessionLocal()
        prompt_service = PromptService()
        ollama_service = OllamaService()
        page_service=PageService()

        try:
            document:Document=session.scalar(
                select(Document).where(Document.document_id==document_id)
            )

            if not document:
                raise ValueError("Document Not Found.")

            pages:list[Page]=page_service.fetch_pages_by_document_id(session,document_id)

            if not pages:
                raise ValueError("Document pages Not Found.")

            markdown_pages = [
                (
                    self._clean_markdown(page.page_markdown),
                    page.page_number
                )
                for page in pages
            ]
            
            if document.document_type_id is None:
                raise ValueError(f"Document type of '{document.document_name}' not found.")

            prompt_details:Prompt=prompt_service.fetch_prompt_by_document_type_id(session,document.document_type_id)

            extracted_data=ollama_service.extract_data(prompt_details.prompt,markdown_pages)

            document.extracted_data = extracted_data

            document.process_stage = "DATA_EXTRACTED"

            session.commit()

            return extracted_data
        except Exception:
            session.rollback()
            raise

        finally:
            session.close()

    def _clean_markdown(self, markdown: str) -> str:
        markdown = markdown.strip()

        if markdown.startswith("```markdown"):
            markdown = markdown.removeprefix("```markdown").strip()

        if markdown.startswith("```"):
            markdown = markdown.removeprefix("```").strip()

        if markdown.endswith("```"):
            markdown = markdown.removesuffix("```").strip()

        return markdown