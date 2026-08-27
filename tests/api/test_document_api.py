from unittest.mock import patch
from uuid import uuid4

@patch("app.main.DocumentService")
def test_upload_document(mock_document_service, client):
    document_id = uuid4()

    mock_document_service.return_value.upload_document.return_value = document_id

    files = {
        "file": ("invoice.pdf", b"fake pdf content", "application/pdf")
    }

    response = client.post("/documents", files=files)

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["filename"] == "invoice.pdf"
    assert response_data["Content_type"] == "application/pdf"
    assert response_data["document_id"] == str(document_id)

    mock_document_service.return_value.upload_document.assert_called_once_with(
        "invoice.pdf",
        b"fake pdf content"
    )


@patch("app.main.DocumentService")
def test_upload_document_conflict(mock_document_service, client):
    mock_document_service.return_value.upload_document.side_effect = ValueError(
        "Document already exists"
    )

    files = {
        "file": ("invoice.pdf", b"fake pdf content", "application/pdf")
    }

    response = client.post("/documents", files=files)

    assert response.status_code == 409
    assert response.json() == {"detail": "Document already exists"}