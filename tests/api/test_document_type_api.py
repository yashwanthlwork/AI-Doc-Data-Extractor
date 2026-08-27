from unittest.mock import patch;
from unittest.mock import patch
from uuid import uuid4

@patch("app.main.DocumentTypeService")
def test_create_document_type(mock_document_type_service, client):
    expected_response = {
        "id": "123",
        "name": "Invoice",
        "description": "Invoice document"
    }

    mock_document_type_service.return_value.create_document_type.return_value = (
        expected_response
    )

    response = client.post(
        "/document-types",
        params={
            "document_type_name": "Invoice",
            "document_type_description": "Invoice document"
        }
    )

    assert response.status_code == 200
    assert response.json() == expected_response

    mock_document_type_service.return_value.create_document_type.assert_called_once_with(
        "Invoice",
        "Invoice document"
    )


@patch("app.main.DocumentTypeService")
def test_create_document_type_invalid(mock_document_type_service, client):
    mock_document_type_service.return_value.create_document_type.side_effect = (
        ValueError("Document type already exists")
    )

    response = client.post(
        "/document-types",
        params={
            "document_type_name": "Invoice",
            "document_type_description": "Invoice document"
        }
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Document type already exists"
    }

@patch("app.main.DocumentTypeService")
def test_get_document_types(mock_document_type_service, client):
    expected_response = [
        {
            "id": "1",
            "name": "INVOICE",
            "description": "Invoice document"
        },
        {
            "id": "2",
            "name": "RECEIPT",
            "description": "Receipt document"
        }
    ]

    mock_document_type_service.return_value.get_all_document_types.return_value = (
        expected_response
    )

    response = client.get("/document-types")

    assert response.status_code == 200
    assert response.json() == expected_response

    mock_document_type_service.return_value.get_all_document_types.assert_called_once_with()


@patch("app.main.DocumentTypeService")
def test_get_document_types(mock_document_type_service, client):
    document_type_1 = {
        "document_type_id": str(uuid4()),
        "document_type_name": "INVOICE",
        "description": "Invoice document"
    }

    document_type_2 = {
        "document_type_id": str(uuid4()),
        "document_type_name": "RECEIPT",
        "description": "Receipt document"
    }

    mock_document_type_service.return_value.get_all_document_types.return_value = [
        document_type_1,
        document_type_2
    ]

    response = client.get("/document-types")

    assert response.status_code == 200
    assert response.json() == [
        document_type_1,
        document_type_2
    ]

    mock_document_type_service.return_value.get_all_document_types.assert_called_once_with()