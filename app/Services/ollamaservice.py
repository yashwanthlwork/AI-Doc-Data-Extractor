from ollama import Client
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.DBModels.document_type import DocumentType


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

    def extract_markdown(self, page_png: bytes):
        prompt=self._load_markdown_prompt()
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

    def classify_document(self,session: Session,page_markdown: str,document_types: list[str] | None = None):        
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

    