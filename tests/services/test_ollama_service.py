from app.Services.ollamaservice import OllamaService
from unittest.mock import MagicMock
import pytest


def test_clean_json_response():
    service = OllamaService()

    content = '```json\n{"invoice_number": "INV-001"}\n```'

    result = service._clean_json_response(content)

    assert result == '{"invoice_number": "INV-001"}'

def test_extract_markdown():
    service = OllamaService()

    service.client = MagicMock()

    mock_response = MagicMock()
    mock_response.message.content = "# Invoice\nInvoice Number: INV-001"

    service.client.chat.return_value = mock_response

    page_png = b"fake png content"

    result = service.extract_markdown(page_png)

    assert result == "# Invoice\nInvoice Number: INV-001"

    service.client.chat.assert_called_once()


def test_classify_document_with_document_types():
    service = OllamaService()

    service.client = MagicMock()

    mock_response = MagicMock()
    mock_response.message.content = "invoice"

    service.client.chat.return_value = mock_response

    document_types = ["Invoice", "Receipt"]
    page_markdown = "# Invoice\nInvoice Number: INV-001"

    result = service.classify_document(
        None,
        page_markdown,
        document_types
    )

    assert result == "INVOICE"

    service.client.chat.assert_called_once()

def test_classify_document_without_document_types():
    service = OllamaService()

    service.client = MagicMock()

    mock_response = MagicMock()
    mock_response.message.content = "receipt"

    service.client.chat.return_value = mock_response

    session = MagicMock()
    session.scalars.return_value.all.return_value = [
        "Invoice",
        "Receipt"
    ]

    page_markdown = "# Receipt\nReceipt Number: REC-001"

    result = service.classify_document(
        session,
        page_markdown
    )

    assert result == "RECEIPT"

    session.scalars.assert_called_once()
    service.client.chat.assert_called_once()

def test_extract_data_success():
    service = OllamaService()

    service.client = MagicMock()

    mock_response = MagicMock()
    mock_response.message.content = (
        '[{"invoice_number": "INV-001", "total": 500}]'
    )

    service.client.chat.return_value = mock_response

    markdown_pages = [
        ("# Invoice\nInvoice Number: INV-001\nTotal: 500", 1)
    ]

    result = service.extract_data(
        "Extract invoice number and total.",
        markdown_pages
    )

    assert result == [
        {
            "invoice_number": "INV-001",
            "total": 500
        }
    ]

    service.client.chat.assert_called_once()

def test_extract_data_invalid_json():
    service = OllamaService()

    service.client = MagicMock()

    mock_response = MagicMock()
    mock_response.message.content = "This is not valid JSON"

    service.client.chat.return_value = mock_response

    markdown_pages = [
        ("# Invoice\nInvoice Number: INV-001", 1)
    ]

    with pytest.raises(
        ValueError,
        match="Page 1: Invalid JSON returned by LLM."
    ):
        service.extract_data(
            "Extract invoice number.",
            markdown_pages
        )