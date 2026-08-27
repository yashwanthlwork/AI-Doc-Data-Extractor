from app.Services.pageservice import PageService
from unittest.mock import MagicMock, patch
from uuid import uuid4
import pytest


def test_fetch_pages_by_document_id_not_found():
    service = PageService()

    session = MagicMock()
    session.scalars.return_value.all.return_value = []

    document_id = uuid4()

    with pytest.raises(
        ValueError,
        match="No pages found for this document"
    ):
        service.fetch_pages_by_document_id(
            session,
            document_id
        )


def test_fetch_pages_by_document_id_success():
    service = PageService()

    session = MagicMock()

    expected_pages = [
        MagicMock(),
        MagicMock()
    ]

    session.scalars.return_value.all.return_value = expected_pages

    document_id = uuid4()

    result = service.fetch_pages_by_document_id(
        session,
        document_id
    )

    assert result == expected_pages
    session.scalars.assert_called_once()

def test_upload_pages_document_not_found():
    service = PageService()

    session = MagicMock()
    session.scalar.return_value = None

    document_id = uuid4()

    with patch(
        "app.Services.pageservice.SessionLocal",
        return_value=session
    ):
        with pytest.raises(
            ValueError,
            match="Document not found"
        ):
            service.upload_pages(document_id)

    session.rollback.assert_called_once()
    session.close.assert_called_once()

def test_upload_pages_success():
    service = PageService()

    session = MagicMock()

    document = MagicMock()
    document.document_id = uuid4()
    document.document_bytes = b"fake pdf"

    session.scalar.return_value = document

    page1 = MagicMock()
    page1.get_pixmap.return_value.tobytes.return_value = b"png-page-1"

    page2 = MagicMock()
    page2.get_pixmap.return_value.tobytes.return_value = b"png-page-2"

    pdf = MagicMock()
    pdf.__iter__.return_value = iter([page1, page2])

    with patch(
        "app.Services.pageservice.SessionLocal",
        return_value=session
    ), patch(
        "app.Services.pageservice.pymupdf.open",
        return_value=pdf
    ):
        service.upload_pages(document.document_id)

    assert document.total_page_number == 2
    assert document.process_stage == "PAGES_CREATED"

    assert session.add.call_count == 2
    session.commit.assert_called_once()
    session.close.assert_called_once()

def test_extract_markdown_no_pages():
    service = PageService()

    session = MagicMock()

    document = MagicMock()
    session.scalar.return_value = document
    session.scalars.return_value.all.return_value = []

    document_id = uuid4()

    with patch(
        "app.Services.pageservice.SessionLocal",
        return_value=session
    ):
        with pytest.raises(
            ValueError,
            match="No pages found for this document"
        ):
            service.extract_markdown(document_id)

    session.rollback.assert_called_once()
    session.close.assert_called_once()

def test_extract_markdown_success():
    service = PageService()

    session = MagicMock()

    document = MagicMock()

    page1 = MagicMock()
    page1.page_png = b"page-1"

    page2 = MagicMock()
    page2.page_png = b"page-2"

    session.scalar.return_value = document
    session.scalars.return_value.all.return_value = [page1, page2]

    ollama_service = MagicMock()
    ollama_service.extract_markdown.side_effect = [
        "# Page 1",
        "# Page 2"
    ]

    document_id = uuid4()

    with patch(
        "app.Services.pageservice.SessionLocal",
        return_value=session
    ), patch(
        "app.Services.pageservice.OllamaService",
        return_value=ollama_service
    ):
        service.extract_markdown(document_id)

    assert page1.page_markdown == "# Page 1"
    assert page2.page_markdown == "# Page 2"

    assert page1.process_stage == "MARKDOWN_EXTRACTED"
    assert page2.process_stage == "MARKDOWN_EXTRACTED"

    assert document.process_stage == "MARKDOWN_EXTRACTED"

    assert ollama_service.extract_markdown.call_count == 2
    session.commit.assert_called_once()
    session.close.assert_called_once()