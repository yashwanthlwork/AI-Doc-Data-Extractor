from collections import Counter
from uuid import UUID
from sqlalchemy import select
from app.Configuration.DBSession import SessionLocal
from app.DBModels.document import Document
from app.DBModels.document_type import DocumentType
from app.DBModels.page import Page
from app.Services.ollamaservice import OllamaService


class DocumentClassificationService:

    def classify_document(self, document_id: UUID):

        session = SessionLocal()
        ollama_service = OllamaService()

        try:

            pages = session.execute(
                select(Page.page_markdown, Page.page_number)
                .where(Page.document_id == document_id)
                .order_by(Page.page_number)
            ).all()

            if not pages:
                raise ValueError("No pages found for this document.")

            candidate_document_types = None
            previous_winners = None

            while True:

                votes = Counter()

                for page_markdown, _ in pages:

                    predicted_document_type = ollama_service.classify_document(
                        session=session,
                        page_markdown=page_markdown,
                        document_types=candidate_document_types
                    )

                    votes[predicted_document_type] += 1

                highest_vote = max(votes.values())

                winners = [
                    document_type
                    for document_type, vote in votes.items()
                    if vote == highest_vote
                ]

                if len(winners) == 1:
                    winning_document_type = winners[0]
                    break

                if previous_winners == winners:
                    raise ValueError("Unable to resolve document classification tie.")

                previous_winners = winners
                candidate_document_types = winners

            document_type = session.scalar(
                select(DocumentType).where(
                    DocumentType.document_type_name == winning_document_type
                )
            )

            if document_type is None:
                raise ValueError("Document type not found.")

            document = session.scalar(
                select(Document).where(
                    Document.document_id == document_id
                )
            )

            if document is None:
                raise ValueError("Document not found.")

            document.document_type_id = document_type.document_type_id
            document.process_stage = "DOCUMENT_CLASSIFIED"

            session.commit()
            return {
                "document_id": str(document_id),
                "document_type_id": str(document_type.document_type_id),
                "document_type_name": document_type.document_type_name,
                "process_stage": document.process_stage
            }

        except Exception:
            session.rollback()
            raise

        finally:
            session.close()