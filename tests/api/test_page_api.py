from unittest.mock import patch
from uuid import uuid4


@patch("app.main.PageService")
def test_create_pages(mock_page_service, client):
    document_id = uuid4()

    response = client.post(
        f"/documents/{document_id}/pages"
    )

    assert response.status_code == 200
    assert response.json() == {
        "document_id": str(document_id),
        "status": "PAGES_CREATED"
    }

    mock_page_service.return_value.upload_pages.assert_called_once_with(
        document_id
    )

@patch("app.main.PageService")
def test_extract_markdown(mock_page_service, client):
    document_id = uuid4()

    response = client.post(
        f"/documents/{document_id}/markdown"
    )

    assert response.status_code == 200
    assert response.json() == {
        "document_id": str(document_id),
        "status": "MARKDOWN_EXTRACTED"
    }

    mock_page_service.return_value.extract_markdown.assert_called_once_with(
        document_id
    )

def test_create_pages_invalid_document_id(client):
    response = client.post(
        "/documents/not-a-valid-uuid/pages"
    )

    assert response.status_code == 422

def test_extract_markdown_invalid_document_id(client):
    response = client.post(
        "/documents/not-a-valid-uuid/markdown"
    )

    assert response.status_code == 422