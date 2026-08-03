from ollama import Client
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.DBModels.document_type import DocumentType
import json
from typing import Any

class OllamaService:
    def __init__(self):
        self.model = "gemma3:4b"
        self.client = Client()

    def _load_markdown_prompt(self):
        with open("app/Prompts/markdown_extraction.txt", "r") as file:
            prompt = file.read()
        return prompt
    
    def _load_classification_prompt(self):
        with open("app/Prompts/document_classification.txt", "r") as file:
            prompt = file.read()
        return prompt
    
    def _load_document_extraction_rules(self):
        with open("app/Prompts/document_extraction_rules.txt", "r") as file:
            prompt = file.read()
        return prompt


    def extract_markdown(self, page_png: bytes):
        prompt = self._load_markdown_prompt()
        response = self.client.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                    "images": [
                        page_png
                    ]
                }
            ]
        )
        markdown = response.message.content

        return markdown

    def classify_document(self, session: Session, page_markdown: str, document_types: list[str] | None = None):        
        prompt = self._load_classification_prompt()
        if document_types is None:
            document_types = session.scalars(
                select(DocumentType.document_type_name)
                .order_by(DocumentType.document_type_name)
            ).all()
        document_types_string = ", ".join(document_types)

        final_prompt = (
            prompt
            .replace("{DOCUMENT_TYPES}", document_types_string)
            .replace("{MARKDOWN}", page_markdown)
        )

        response = self.client.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": final_prompt
                }
            ]
        )

        predicted_document_type = response.message.content.strip().upper()

        return predicted_document_type

    def extract_data(self, extraction_prompt: str, markdown_pages: list[tuple[str, int]]) -> list[dict[str, Any]]:
        extracted_records: list[dict[str, Any]] = []
        rules = self._load_document_extraction_rules()
        for page_markdown, page_number in markdown_pages:
            final_prompt = f"""
                {extraction_prompt}

                {rules}

                Current Page Number:
                {page_number}

                Current Extracted Records:
                {json.dumps(extracted_records, indent=2)}

                Current Page Markdown:
                {page_markdown}
                """

            response = self.client.chat(
                model=self.model,
                format="json",
                messages=[
                    {
                        "role": "user",
                        "content": final_prompt
                    }
                ]
            )

            try:
                content = self._clean_json_response(response.message.content)
                
                content = content.strip()

                extracted_records = json.loads(content)

                if isinstance(extracted_records, dict):
                    extracted_records = [extracted_records]

                if not isinstance(extracted_records, list):
                    raise ValueError(
                        f"Page {page_number}: LLM did not return a JSON array."
                    )

                if not all(isinstance(record, dict) for record in extracted_records):
                    raise ValueError("JSON array must contain JSON objects only.")

            except json.JSONDecodeError as ex:
                raise ValueError(
                    f"Page {page_number}: Invalid JSON returned by LLM.\n{ex}"
                )

        return extracted_records

    def _clean_json_response(self, content: str) -> str:
        return (
            content.strip()
            .removeprefix("```json")
            .removeprefix("```")
            .removesuffix("```")
            .strip()
        )
        
        

    