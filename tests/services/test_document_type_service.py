from app.Services.documenttypeservice import DocumentTypeService
from unittest.mock import MagicMock, patch
from app.DBModels.document_type import DocumentType
import pytest


def test_create_document_type_empty_name():
    service = DocumentTypeService()

    with pytest.raises(
        ValueError,
        match="Document type name cannot be empty."
    ):
        service.create_document_type(
            "",
            "Invoice document"
        )


def test_create_document_type_empty_description():
    service = DocumentTypeService()

    with pytest.raises(
        ValueError,
        match="Document type description cannot be empty."
    ):
        service.create_document_type(
            "Invoice",
            ""
        )

def test_create_document_type_duplicate():
    service = DocumentTypeService()

    session = MagicMock()
    existing_document_type = DocumentType(
        document_type_name="INVOICE",
        description="Invoice document"
    )
    session.scalar.return_value = existing_document_type

    with patch(
        "app.Services.documenttypeservice.SessionLocal",
        return_value=session
    ):
        with pytest.raises(
            ValueError,
            match="Document type already exists."
        ):
            service.create_document_type(
                "Invoice",
                "Invoice document"
            )

    session.rollback.assert_called_once()
    session.close.assert_called_once()

def test_create_document_type_success():
    service = DocumentTypeService()

    session = MagicMock()
    session.scalar.return_value = None

    with patch(
        "app.Services.documenttypeservice.SessionLocal",
        return_value=session
    ):
        result = service.create_document_type(
            " invoice ",
            " Invoice document "
        )

    assert result.document_type_name == "INVOICE"
    assert result.description == "Invoice document"

    session.add.assert_called_once()
    session.commit.assert_called_once()
    session.refresh.assert_called_once_with(result)
    session.close.assert_called_once()

def test_check_document_type_exists_true():
    service = DocumentTypeService()

    session = MagicMock()
    session.scalar.return_value = MagicMock()

    result = service._check_document_type_exists(
        session,
        "INVOICE"
    )

    assert result is True
    session.scalar.assert_called_once()

def test_check_document_type_exists_false():
    service = DocumentTypeService()

    session = MagicMock()
    session.scalar.return_value = None

    result = service._check_document_type_exists(
        session,
        "INVOICE"
    )

    assert result is False
    session.scalar.assert_called_once()