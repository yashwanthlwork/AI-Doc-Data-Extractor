from app.Services.promptservice import PromptService
from unittest.mock import MagicMock, patch
from uuid import uuid4
import pytest

def test_create_prompt_empty_name():
    service = PromptService()

    with pytest.raises(ValueError, match="Prompt name cannot be empty."):
        service.create_prompt(
            "",
            "Extract invoice number",
            uuid4()
        )


def test_create_prompt_empty_prompt():
    service = PromptService()

    with pytest.raises(ValueError, match="Prompt cannot be empty."):
        service.create_prompt(
            "Invoice Prompt",
            "",
            uuid4()
        )


def test_create_prompt_empty_document_type():
    service = PromptService()

    with pytest.raises(ValueError, match="Document type cannot be empty."):
        service.create_prompt(
            "Invoice Prompt",
            "Extract invoice number",
            None
        )

def test_fetch_prompt_by_prompt_id_invalid_id():
    service = PromptService()

    with pytest.raises(ValueError, match="Invalid Prompt ID."):
        service.fetch_prompt_by_prompt_id(None, None)

def test_fetch_prompt_by_prompt_id_not_found():
    service = PromptService()

    session = MagicMock()
    session.scalar.return_value = None

    prompt_id = uuid4()

    with pytest.raises(
        ValueError,
        match="Given Prompt ID does not exist."
    ):
        service.fetch_prompt_by_prompt_id(session, prompt_id)

    session.scalar.assert_called_once()

def test_fetch_prompt_by_prompt_id_success():
    service = PromptService()

    session = MagicMock()
    expected_prompt = MagicMock()

    session.scalar.return_value = expected_prompt

    prompt_id = uuid4()

    result = service.fetch_prompt_by_prompt_id(
        session,
        prompt_id
    )

    assert result is expected_prompt

    session.scalar.assert_called_once()

def test_create_prompt_document_type_not_found():
    service = PromptService()

    session = MagicMock()
    session.scalar.return_value = None

    with patch("app.Services.promptservice.SessionLocal", return_value=session):
        with pytest.raises(
            ValueError,
            match="Document type does not exist."
        ):
            service.create_prompt(
                "Invoice Prompt",
                "Extract invoice number",
                uuid4()
            )

    session.rollback.assert_called_once()
    session.close.assert_called_once()

def test_create_prompt_duplicate_name():
    service = PromptService()

    session = MagicMock()

    document_type = MagicMock()
    existing_prompt = MagicMock()

    session.scalar.side_effect = [
        document_type,
        existing_prompt
    ]

    with patch("app.Services.promptservice.SessionLocal", return_value=session):
        with pytest.raises(
            ValueError,
            match="Prompt name already exists."
        ):
            service.create_prompt(
                "Invoice Prompt",
                "Extract invoice number",
                uuid4()
            )

    session.rollback.assert_called_once()
    session.close.assert_called_once()


def test_create_prompt_duplicate_document_type():
    service = PromptService()

    session = MagicMock()

    document_type = MagicMock()

    session.scalar.side_effect = [
        document_type,
        None,
        MagicMock()
    ]

    with patch("app.Services.promptservice.SessionLocal", return_value=session):
        with pytest.raises(
            ValueError,
            match="A prompt already exists for this document type."
        ):
            service.create_prompt(
                "Invoice Prompt",
                "Extract invoice number",
                uuid4()
            )

    session.rollback.assert_called_once()
    session.close.assert_called_once()


def test_create_prompt_success():
    service = PromptService()

    session = MagicMock()

    session.scalar.side_effect = [
        MagicMock(),
        None,
        None
    ]

    with patch("app.Services.promptservice.SessionLocal", return_value=session):
        result = service.create_prompt(
            " invoice prompt ",
            " Extract invoice number ",
            uuid4()
        )

    created_prompt = session.add.call_args.args[0]

    assert created_prompt.prompt_name == "INVOICE PROMPT"
    assert created_prompt.prompt == "Extract invoice number"

    session.add.assert_called_once()
    session.commit.assert_called_once()
    session.refresh.assert_called_once_with(created_prompt)
    session.close.assert_called_once()