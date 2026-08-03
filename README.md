# Python AI Document Intelligence

This is a project I started to better understand how Large Language Models (LLMs) can be used to automate document processing.

While working on enterprise applications, I realized that a lot of business processes still depend on manually reading PDF documents and entering the required information into another system. I wanted to understand how this entire process works, so I decided to build it myself from scratch.

Instead of using a ready-made solution, I wanted to implement every major step involved in an Intelligent Document Processing (IDP) pipeline. This project gave me the opportunity to learn how different technologies work together—from handling PDF documents and databases to integrating AI models for document understanding and structured data extraction.

The current implementation takes a PDF document, processes it step by step, identifies the document type, and extracts structured JSON data using configurable prompts.

---

# What I've Built

Currently, the project can:

- Upload PDF documents.
- Store uploaded documents in PostgreSQL.
- Split PDFs into individual pages.
- Convert each page into a PNG image.
- Generate markdown from page images using Ollama Vision.
- Classify the document type using an LLM.
- Maintain configurable document types.
- Maintain configurable extraction prompts.
- Extract structured JSON based on the classified document type.
- Store the extracted JSON in the database.

---

# How It Works

Every document follows the same processing flow.

```text
Upload PDF
      │
      ▼
Store Document
      │
      ▼
Split PDF into Pages
      │
      ▼
Generate PNG Images
      │
      ▼
Extract Markdown
      │
      ▼
Classify Document
      │
      ▼
Load Extraction Prompt
      │
      ▼
Extract Structured Data
      │
      ▼
Store Extracted JSON
```

---

# Technology Stack

| Category | Technology |
|----------|------------|
| Language | Python 3 |
| Framework | FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Database Migration | Alembic |
| PDF Processing | PyMuPDF |
| AI Runtime | Ollama |
| AI Model | Gemma 3 (4B) |
| Data Format | JSON |

---

# Project Structure

```text
Python_AI_DOC_INTELLIGENCE/
│
├── alembic/              # Database migrations
├── app/
│   ├── Configuration/    # Database configuration
│   ├── DBModels/         # SQLAlchemy models
│   ├── Prompts/          # Prompt templates
│   ├── Services/         # Business logic
│   └── main.py           # FastAPI application
│
├── docs/
├── .env
├── requirements.txt
└── README.md
```

---


# Prerequisites

Before running this project, make sure the following software is installed on your machine.

- Python 3.14.6 (I have used)
- PostgreSQL
- Ollama

You can verify the installation using:

```bash
python3 --version
psql --version
ollama --version
```

Before starting the application:

- Make sure your PostgreSQL server is running.
- Make sure the Ollama service is running.

If any of the commands above fail, install the missing software before continuing with the setup.

---

# Running the Project

> **Note:** I developed and tested this project on **macOS**, so the commands below are for macOS.

## 1. Clone the repository

```bash
git clone https://github.com/<your-github-username>/Python_AI_DOC_INTELLIGENCE.git

cd Python_AI_DOC_INTELLIGENCE
```

---

## 2. Create a virtual environment

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

---

## 3. Install the Project Dependencies

All the Python packages required to run this project are listed in the `requirements.txt` file.

Install everything with a single command:

```bash
pip install -r requirements.txt
```

This will install all the required libraries, including:

- FastAPI
- SQLAlchemy
- PostgreSQL driver (`psycopg`)
- Alembic
- PyMuPDF
- Ollama Python SDK
- Uvicorn
- and the remaining dependencies required by the project.

---

## 4. Create the Database

Create a PostgreSQL database for the project.

For example:

```sql
CREATE DATABASE document_intelligence;
```

Then create a `.env` file and configure the database connection.

Example:

```text
DATABASE_URL=postgresql://username:password@localhost:5432/document_intelligence
```

---

## 5. Apply database migrations

```bash
alembic upgrade head
```

---

## 6. Install the Ollama Model

If this is your first time using Ollama, download the model required by this project.

```bash
ollama pull gemma3:4b
```

Before starting the application, make sure the Ollama service is running.

You can verify it using:

```bash
ollama list
```

---

## 7. Start the Application

Start the FastAPI server.

```bash
uvicorn app.main:app --reload
```

Once the server starts successfully, open the Swagger UI in your browser.

```
http://127.0.0.1:8000/docs
```

Swagger provides an interactive interface where you can test every API exposed by the application.

---

# API Endpoints

Once the application is running, FastAPI automatically generates Swagger documentation.

Open the following URL in your browser:

```
http://127.0.0.1:8000/docs
```

The APIs below follow the normal document processing flow.

---

## 1. Upload Document

**POST** `/upload`

This is the starting point of the document processing pipeline.

Upload a PDF document using `multipart/form-data`.

### What it does

- Accepts a PDF document.
- Reads the PDF as bytes.
- Creates a new document in the database.
- Returns the generated Document ID.

### Input

- PDF file

### Returns

```json
{
  "filename": "...",
  "Content_type": "application/pdf",
  "document_id": "..."
}
```

The returned **Document ID** is required for the remaining APIs.

---

## 2. Create Pages

**POST** `/documents/{document_id}/create-pages`

Once the document is uploaded, This endpoint reads the uploaded PDF and creates one page record for every page in the document.

### What it does

- Reads the uploaded PDF.
- Splits the PDF into individual pages.
- Converts every page into a PNG image.
- Stores each page in the Pages table.
- Updates the document processing stage.

### Path Parameter

- `document_id`

### Returns

```json
{
  "document_id": "...",
  "status": "PAGES_CREATED"
}
```

---

## 3. Extract Markdown

**POST** `/documents/{document_id}/extract-markdown`

This endpoint generates markdown for every page created in the previous step.

### What it does

- Reads each PNG image.
- Sends the image to Ollama Vision.
- Generates markdown.
- Stores the markdown for every page.
- Updates the processing stage.

### Path Parameter

- `document_id`

### Returns

```json
{
  "document_id": "...",
  "status": "MARKDOWN_EXTRACTED"
}
```

---

## 4. Create Document Type

**POST** `/document-types`

Creates a new document type supported by the application.

### Example

- Invoice
- Purchase Order
- Receipt

### Parameters

- `document_type_name`
- `document_type_description`

---

## 5. View Document Types

**GET** `/document-types`

Returns all configured document types.

This list is later used during document classification.

---

## 6. Create Prompt

**POST** `/prompts`

Creates a new extraction prompt.

Each prompt is linked to a document type.

### Parameters

- `prompt_name`
- `prompt`
- `document_type_id`

---

## 7. View Prompts

**GET** `/prompts`

Returns all configured prompts.

These prompts are later used during structured data extraction.

---

## 8. Update Prompt

**PATCH** `/prompts`

Updates the prompt text for an existing prompt.

### Parameters

- `prompt_id`
- `prompt`

---

## 9. Update Prompt Mapping

**PATCH** `/prompts`

Changes the document type associated with a prompt.

### Parameters

- `prompt_id`
- `document_type_id`

> **Note:** At the moment, both update operations use the same endpoint with different parameters. This works for development, but separating them into different routes would make the API clearer.

---

## 10. Classify Document

**POST** `/classify-document`

Classifies the uploaded document using the markdown generated earlier.

### What it does

- Reads markdown from all pages.
- Retrieves the configured document types.
- Uses Ollama to identify the document type.
- Saves the predicted document type in the database.

### Parameter

- `document_id`

### Returns

The predicted document type.

---

## 11. Extract Structured Data

**POST** `/documents/{document_id}/extract-data`

This is the final step of the pipeline.

### What it does

- Reads the page markdown.
- Retrieves the extraction prompt for the classified document type.
- Sends the markdown and prompt to Ollama.
- Extracts structured JSON.
- Stores the extracted JSON in the Documents table.

### Path Parameter

- `document_id`

### Returns

The extracted JSON data.

---

# Typical Workflow

When testing the project, call the APIs in the following order:

1. Upload Document
2. Create Pages
3. Extract Markdown
4. Create Document Types *(one-time setup)*
5. Create Prompt *(one-time setup)*
6. Classify Document
7. Extract Structured Data

> **Note:** Document Types and Prompts only need to be configured once. After they are created, the same configuration can be reused for processing multiple documents of the same type.
---

# Project Documentation

I have documented the project in a few simple documents that explain the idea behind it and how it is implemented.

- `docs/Purpose.md` — Why I started this project.
- `docs/PlannedSolution.md` — The approach I planned before implementation.
- `docs/Architecture.md` — A simple overview of how the application is organized.

---

# Current Status

The core Intelligent Document Processing (IDP) pipeline has been implemented.

The application currently supports:

- Uploading PDF documents.
- Splitting PDFs into individual pages.
- Generating PNG images for each page.
- Extracting markdown using Ollama Vision.
- Managing document types.
- Managing extraction prompts.
- Classifying documents using AI.
- Extracting structured JSON data using configurable prompts.
- Storing the extracted JSON in PostgreSQL.

The project will continue to evolve with additional document types, improved extraction quality, and further enhancements to the overall document processing workflow.

---

# Thank You

If you took the time to explore this project, thank you.

I built this project to learn, experiment, and gain a deeper understanding of AI-powered document processing. If you have suggestions, ideas, or feedback, I'd be happy to hear them.