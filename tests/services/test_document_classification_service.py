from app.Services.documentclassificationservice import DocumentClassificationService
from unittest.mock import MagicMock, patch
from app.DBModels.document import Document
from app.DBModels.document_type import DocumentType
import pytest
from uuid import uuid4


def test_classify_document_no_pages():
    service = DocumentClassificationService()

    session = MagicMock()
    session.execute.return_value.all.return_value = []

    with patch(
        "app.Services.documentclassificationservice.SessionLocal",
        return_value=session
    ):
        with pytest.raises(
            ValueError,
            match="No pages found for this document."
        ):
            service.classify_document(MagicMock())

    session.rollback.assert_called_once()
    session.close.assert_called_once()


def test_classify_document_success():
    service = DocumentClassificationService()

    document_id = uuid4()
    document_type_id = uuid4()

    session = MagicMock()

    session.execute.return_value.all.return_value = [
        ("invoice page 1", 1),
        ("invoice page 2", 2)
    ]

    document_type = DocumentType(
        document_type_id=document_type_id,
        document_type_name="INVOICE",
        description="Invoice document"
    )

    document = Document(
        document_id=document_id,
        document_type_id=None,
        process_stage="UPLOADED"
    )

    session.scalar.side_effect = [
        document_type,
        document
    ]

    ollama_service = MagicMock()
    ollama_service.classify_document.side_effect = [
        "INVOICE",
        "INVOICE"
    ]

    with patch(
        "app.Services.documentclassificationservice.SessionLocal",
        return_value=session
    ), patch(
        "app.Services.documentclassificationservice.OllamaService",
        return_value=ollama_service
    ):
        result = service.classify_document(document_id)

    assert result == {
        "document_id": str(document_id),
        "document_type_id": str(document_type_id),
        "document_type_name": "INVOICE",
        "process_stage": "DOCUMENT_CLASSIFIED"
    }

    assert document.document_type_id == document_type_id
    assert document.process_stage == "DOCUMENT_CLASSIFIED"

    assert ollama_service.classify_document.call_count == 2
    session.commit.assert_called_once()
    session.close.assert_called_once()


def test_classify_document_resolves_tie():
    service = DocumentClassificationService()

    document_id = uuid4()
    document_type_id = uuid4()

    session = MagicMock()

    session.execute.return_value.all.return_value = [
        ("page 1", 1),
        ("page 2", 2)
    ]

    document_type = DocumentType(
        document_type_id=document_type_id,
        document_type_name="INVOICE",
        description="Invoice document"
    )

    document = Document(
        document_id=document_id,
        document_type_id=None,
        process_stage="UPLOADED"
    )

    session.scalar.side_effect = [
        document_type,
        document
    ]

    ollama_service = MagicMock()

    # First round: tie
    # Second round: INVOICE wins
    ollama_service.classify_document.side_effect = [
        "INVOICE",
        "RECEIPT",
        "INVOICE",
        "INVOICE"
    ]

    with patch(
        "app.Services.documentclassificationservice.SessionLocal",
        return_value=session
    ), patch(
        "app.Services.documentclassificationservice.OllamaService",
        return_value=ollama_service
    ):
        result = service.classify_document(document_id)

    assert result["document_type_name"] == "INVOICE"
    assert result["process_stage"] == "DOCUMENT_CLASSIFIED"

    assert ollama_service.classify_document.call_count == 4
    session.commit.assert_called_once()
    session.close.assert_called_once()


def test_classify_document_unresolvable_tie():
    service = DocumentClassificationService()

    document_id = uuid4()

    session = MagicMock()

    session.execute.return_value.all.return_value = [
        ("page 1", 1),
        ("page 2", 2)
    ]

    ollama_service = MagicMock()

    # Same tie occurs twice
    ollama_service.classify_document.side_effect = [
        "INVOICE",
        "RECEIPT",
        "INVOICE",
        "RECEIPT"
    ]

    with patch(
        "app.Services.documentclassificationservice.SessionLocal",
        return_value=session
    ), patch(
        "app.Services.documentclassificationservice.OllamaService",
        return_value=ollama_service
    ):
        with pytest.raises(
            ValueError,
            match="Unable to resolve document classification tie."
        ):
            service.classify_document(document_id)

    session.rollback.assert_called_once()
    session.close.assert_called_once()
    session.commit.assert_not_called()


def test_classify_document_type_not_found():
    service = DocumentClassificationService()

    document_id = uuid4()

    session = MagicMock()

    session.execute.return_value.all.return_value = [
        ("invoice page", 1)
    ]

    # DocumentType lookup returns None
    session.scalar.return_value = None

    ollama_service = MagicMock()
    ollama_service.classify_document.return_value = "INVOICE"

    with patch(
        "app.Services.documentclassificationservice.SessionLocal",
        return_value=session
    ), patch(
        "app.Services.documentclassificationservice.OllamaService",
        return_value=ollama_service
    ):
        with pytest.raises(
            ValueError,
            match="Document type not found."
        ):
            service.classify_document(document_id)

    session.rollback.assert_called_once()
    session.close.assert_called_once()


def test_classify_document_document_not_found():
    service = DocumentClassificationService()

    document_id = uuid4()
    document_type_id = uuid4()

    session = MagicMock()

    session.execute.return_value.all.return_value = [
        ("invoice page", 1)
    ]

    document_type = DocumentType(
        document_type_id=document_type_id,
        document_type_name="INVOICE",
        description="Invoice document"
    )

    # First scalar -> DocumentType
    # Second scalar -> Document
    session.scalar.side_effect = [
        document_type,
        None
    ]

    ollama_service = MagicMock()
    ollama_service.classify_document.return_value = "INVOICE"

    with patch(
        "app.Services.documentclassificationservice.SessionLocal",
        return_value=session
    ), patch(
        "app.Services.documentclassificationservice.OllamaService",
        return_value=ollama_service
    ):
        with pytest.raises(
            ValueError,
            match="Document not found."
        ):
            service.classify_document(document_id)

    session.rollback.assert_called_once()
    session.close.assert_called_once()