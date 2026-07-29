from ollama import Client

class OllamaService:
    def __init__(self):
        self.model = "gemma3:4b"
        self.client = Client()

    def _load_prompt(self):
        with open("app/Prompts/markdown_extraction.txt", "r") as file:
            prompt = file.read()
        return prompt

    def extract_markdown(self, page_png: bytes):
        prompt=self._load_prompt()
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

    