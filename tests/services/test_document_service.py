from app.Services.documentservice import DocumentService
from unittest.mock import MagicMock, patch
from app.DBModels.document import Document
import pytest


def test_upload_document_success():
    service = DocumentService()

    session = MagicMock()
    session.scalar.return_value = None

    document_id = "test-document-id"

    def refresh_side_effect(document):
        document.document_id = document_id

    session.refresh.side_effect = refresh_side_effect

    with patch(
        "app.Services.documentservice.SessionLocal",
        return_value=session
    ):
        result = service.upload_document(
            "invoice.pdf",
            b"test pdf content"
        )

    assert result == document_id

    session.add.assert_called_once()
    session.commit.assert_called_once()
    session.refresh.assert_called_once()
    session.close.assert_called_once()

def test_upload_document_duplicate():
    service = DocumentService()

    session = MagicMock()
    session.scalar.return_value = Document(
        document_name="existing.pdf"
    )

    with patch(
        "app.Services.documentservice.SessionLocal",
        return_value=session
    ):
        with pytest.raises(
            ValueError,
            match="Document already exists."
        ):
            service.upload_document(
                "invoice.pdf",
                b"test pdf content"
            )

    session.rollback.assert_called_once()
    session.close.assert_called_once()

def test_upload_document_database_failure():
    service = DocumentService()

    session = MagicMock()
    session.scalar.return_value = None
    session.commit.side_effect = Exception("Database error")

    with patch(
        "app.Services.documentservice.SessionLocal",
        return_value=session
    ):
        with pytest.raises(
            Exception,
            match="Database error"
        ):
            service.upload_document(
                "invoice.pdf",
                b"test pdf content"
            )

    session.rollback.assert_called_once()
    session.close.assert_called_once()

def test_update_stage_success():
    service = DocumentService()

    session = MagicMock()

    document = Document(
        document_name="invoice.pdf",
        process_stage="UPLOADED"
    )

    session.scalar.return_value = document

    document_id = "test-document-id"

    with patch(
        "app.Services.documentservice.SessionLocal",
        return_value=session
    ):
        with patch.object(
            service,
            "check_document_exists",
            return_value=True
        ):
            service.update_stage(
                document_id,
                "MARKDOWN_EXTRACTED"
            )

    assert document.process_stage == "MARKDOWN_EXTRACTED"

    session.commit.assert_called_once()
    session.close.assert_called_once()

def test_update_stage_invalid_document_id():
    service = DocumentService()

    session = MagicMock()

    with patch(
        "app.Services.documentservice.SessionLocal",
        return_value=session
    ):
        with patch.object(
            service,
            "check_document_exists",
            return_value=False
        ):
            with pytest.raises(
                ValueError,
                match="Invalid document_id"
            ):
                service.update_stage(
                    "invalid-document-id",
                    "MARKDOWN_EXTRACTED"
                )

    session.rollback.assert_called_once()
    session.close.assert_called_once()

def test_update_document_type_success():
    service = DocumentService()

    session = MagicMock()

    document = Document(
        document_name="invoice.pdf"
    )

    session.scalar.return_value = document

    document_id = "document-id"
    document_type_id = "document-type-id"

    with patch(
        "app.Services.documentservice.SessionLocal",
        return_value=session
    ):
        with patch.object(
            service,
            "check_document_exists",
            return_value=True
        ):
            with patch(
                "app.Services.documentservice.DocumentTypeService"
            ) as mock_document_type_service:

                mock_document_type_service.return_value.check_document_type_id_exists.return_value = True

                result = service.update_document_type(
                    document_id,
                    document_type_id
                )

    assert result is document
    assert document.document_type_id == document_type_id

    session.commit.assert_called_once()
    session.refresh.assert_called_once_with(document)
    session.close.assert_called_once()

def test_update_document_type_invalid_document_id():
    service = DocumentService()

    session = MagicMock()

    with patch(
        "app.Services.documentservice.SessionLocal",
        return_value=session
    ):
        with patch.object(
            service,
            "check_document_exists",
            return_value=False
        ):
            with pytest.raises(
                ValueError,
                match="Invalid document_id"
            ):
                service.update_document_type(
                    "invalid-document-id",
                    "document-type-id"
                )

    session.rollback.assert_called_once()
    session.close.assert_called_once()