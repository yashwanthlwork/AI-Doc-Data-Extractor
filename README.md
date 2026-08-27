# AI Document Intelligence API

This is an Intelligent Document Processing (IDP) backend project I built to understand how Large Language Models (LLMs) can be used to automate business document workflows.

While working on enterprise applications, I realized that many business processes still depend on manually reading PDF documents and entering required details into other systems. I wanted to understand how this entire pipeline works under the hood, so I built this API from scratch.

Instead of using a ready-made solution, I implemented the major steps involved in an IDP pipeline—from PDF ingestion and page-by-page image rendering to vision-based markdown extraction, document classification, and prompt-driven structured data extraction using a local LLM.

---

# What I've Built

Currently, the project can:

- Upload PDF documents.
- Store uploaded documents in PostgreSQL.
- Split PDFs into individual pages.
- Convert each page into a PNG image.
- Generate markdown from page images using Ollama Vision.
- Classify documents using an LLM.
- Maintain configurable document types.
- Maintain customizable extraction prompts.
- Dynamically extract structured JSON data based on user-defined prompts.
- Store the extracted JSON in PostgreSQL.

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

Document types and extraction prompts are configuration data that can be created and reused across multiple documents.

---

# Technology Stack

| Category | Technology |
|---|---|
| Language | Python 3.14 |
| Framework | FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Database Migration | Alembic |
| PDF Processing | PyMuPDF |
| AI Runtime | Ollama |
| Ollama Model | `qwen2.5:7b-instruct` |
| AI Integration | Ollama Python SDK |
| Data Format | JSON |
| Containerization | Docker |

---

# Architecture

The application is designed so that the FastAPI application can run either directly on the host machine or inside a Docker container.

PostgreSQL and Ollama are intentionally kept as external dependencies rather than being included in the application container.

```text
                         ┌──────────────────────┐
                         │        Client        │
                         │   Swagger / Postman  │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │  FastAPI Application │
                         │       :8000          │
                         │                      │
                         │  Document Services   │
                         │  Page Services       │
                         │  Classification      │
                         │  Extraction          │
                         └───────┬───────┬──────┘
                                 │       │
                  ┌──────────────┘       └──────────────┐
                  ▼                                     ▼
        ┌──────────────────┐                  ┌──────────────────┐
        │    PostgreSQL    │                  │      Ollama      │
        │                  │                  │                  │
        │  Documents       │                  │ qwen2.5:7b       │
        │  Pages           │                  │ instruct         │
        │  Prompts         │                  │                  │
        │  Document Types  │                  │ :11434           │
        └──────────────────┘                  └──────────────────┘
```

When the FastAPI application runs inside Docker, the external services are accessed through:

```text
host.docker.internal
```

This keeps the application container independent from the database and AI runtime.

---

# Project Structure

```text
Python_AI_DOC_INTELLIGENCE/
│
├── alembic/                    # Database migrations
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
│
├── app/
│   ├── Configuration/          # Application configuration
│   │   ├── Config.py
│   │   ├── DBConfig.py
│   │   └── DBSession.py
│   │
│   ├── DBModels/               # SQLAlchemy models
│   │
│   ├── Prompts/                # Prompt templates and extraction rules
│   │   ├── document_classification.txt
│   │   ├── document_extraction_rules.txt
│   │   └── markdown_extraction.txt
│   │
│   ├── Services/               # Application business logic
│   │
│   └── main.py                 # FastAPI application
│
├── docs/                       # Project documentation
│
├── .dockerignore               # Docker build exclusions
├── .env.example                # Environment configuration template
├── .gitignore
├── Dockerfile
├── alembic.ini
├── requirements.txt
└── README.md
```

Environment files containing actual credentials are intentionally not included in the repository.

---

# Prerequisites

The project supports two ways of running the application:

1. Running the FastAPI application directly with Python.
2. Running the FastAPI application inside Docker.

In both approaches, PostgreSQL and Ollama remain external dependencies.

## For local development

Install:

- Python 3.14
- PostgreSQL
- Ollama

Verify the installations:

```bash
python3 --version
psql --version
ollama --version
```

Make sure:

- PostgreSQL is running.
- Ollama is running.
- The required Ollama model is available.

---

# Environment Configuration

The application uses environment variables for external service configuration.

The repository contains:

```text
.env.example
```

as a configuration template.

Actual environment files such as:

```text
.env
.env.docker
```

are intentionally excluded from Git.

---

## Local Development Configuration

Create a `.env` file in the project root.

Example:

```env
DB_USER=your_postgres_user
DB_PASSWORD=your_postgres_password
DB_BASEURL=localhost:5432
DB_NAME=python_ai_doc_intelligence

OLLAMA_BASE_URL=http://localhost:11434
```

When running the application directly on the host machine, both PostgreSQL and Ollama are accessed through `localhost`.

---

# Running the Project Locally

> I developed and tested this project on macOS, so the commands below are written for macOS.

## 1. Clone the repository

```bash
git clone https://github.com/yashwanthlwork/AI-Document-Intelligence-API.git

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

## 3. Install the project dependencies

All Python dependencies are listed in `requirements.txt`.

Install them with:

```bash
pip install -r requirements.txt
```

---

## 4. Create the PostgreSQL database

Create a PostgreSQL database for the project.

For example:

```sql
CREATE DATABASE python_ai_doc_intelligence;
```

Then configure the `.env` file:

```env
DB_USER=your_postgres_user
DB_PASSWORD=your_postgres_password
DB_BASEURL=localhost:5432
DB_NAME=python_ai_doc_intelligence

OLLAMA_BASE_URL=http://localhost:11434
```

---

## 5. Apply database migrations

Run:

```bash
alembic upgrade head
```

This creates the database schema defined by the project's Alembic migrations.

---

## 6. Install the Ollama model

The project currently uses:

```text
qwen2.5:7b-instruct
```

Pull the model:

```bash
ollama pull qwen2.5:7b-instruct
```

Verify that it is available:

```bash
ollama list
```

Make sure the Ollama service is running before using the AI-related endpoints.

---

## 7. Start the application

Run:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

---

# Running with Docker

The FastAPI application can also be run as a Docker container.

The project intentionally does **not** containerize PostgreSQL or Ollama.

The container contains only the Python/FastAPI application and its dependencies.

```text
Docker Container
┌──────────────────────────────┐
│ FastAPI Application          │
│                              │
│ Python                       │
│ FastAPI                      │
│ SQLAlchemy                   │
│ PyMuPDF                      │
│ Ollama SDK                   │
│                              │
│ Port: 8000                   │
└──────────────┬───────────────┘
               │
               │ host.docker.internal
               │
       ┌───────┴────────┐
       │                │
       ▼                ▼
 PostgreSQL          Ollama
   :5432              :11434
```

This separation keeps the application container lightweight and allows PostgreSQL and Ollama to be managed independently.

---

## 1. Docker prerequisites

Install Docker Desktop.

Verify Docker:

```bash
docker --version
```

Make sure PostgreSQL and Ollama are running on the host machine.

---

## 2. Configure Docker environment

Create a `.env.docker` file in the project root.

Example:

```env
DB_USER=your_postgres_user
DB_PASSWORD=your_postgres_password
DB_BASEURL=host.docker.internal:5432
DB_NAME=python_ai_doc_intelligence

OLLAMA_BASE_URL=http://host.docker.internal:11434
```

### Why `host.docker.internal`?

Inside a Docker container, `localhost` refers to the container itself.

Therefore:

```text
localhost:5432
```

would refer to PostgreSQL inside the container, which is not what this project uses.

Instead, Docker Desktop provides:

```text
host.docker.internal
```

which allows the container to access services running on the host machine.

Therefore:

```env
DB_BASEURL=host.docker.internal:5432
OLLAMA_BASE_URL=http://host.docker.internal:11434
```

---

## 3. Build the Docker image

From the project root:

```bash
docker build -t ai-document-intelligence .
```

Verify the image:

```bash
docker images ai-document-intelligence
```

---

## 4. Run the container

```bash
docker run --env-file .env.docker -p 8000:8000 ai-document-intelligence
```

The API will be available at:

```text
http://localhost:8000
```

Swagger UI:

```text
http://localhost:8000/docs
```

---

## 5. Verify the container

Check running containers:

```bash
docker ps
```

You can also test the root endpoint:

```bash
curl http://localhost:8000/
```

Expected response:

```json
{
  "status": "running"
}
```

---

## 6. Stop the container

If the container is running in the foreground:

```text
Ctrl+C
```

Or find the container:

```bash
docker ps
```

and stop it:

```bash
docker stop <container_id>
```

---

# Docker Design Decisions

This project intentionally uses a **single application container**.

The following components remain external.

### PostgreSQL

PostgreSQL stores:

- Documents
- Pages
- Document types
- Prompts
- Extracted JSON data
- Other application data

### Ollama

Ollama provides the local LLM runtime used for:

- Markdown extraction from page images
- Document classification
- Structured data extraction

### Why they are not containerized

The purpose of Docker here is to demonstrate containerization of the **application itself**, while keeping infrastructure dependencies independently configurable.

This allows someone cloning the project to use their own PostgreSQL and Ollama installations without modifying the application image.

---

# API Endpoints

Once the application is running, FastAPI automatically generates Swagger documentation.

Open:

```text
http://localhost:8000/docs
```

The following endpoints represent the current API.

---

## 1. Root

**GET**

```text
/
```

Returns the application status.

Example response:

```json
{
  "status": "running"
}
```

---

## 2. Upload Document

**POST**

```text
/documents
```

Uploads a document using `multipart/form-data`.

### What it does

- Accepts the uploaded file.
- Reads the document as bytes.
- Stores the document in PostgreSQL.
- Returns the generated document ID.

### Input

- `file`

### Example response

```json
{
  "filename": "invoice.pdf",
  "Content_type": "application/pdf",
  "document_id": "..."
}
```

The returned `document_id` is used by the remaining document-processing endpoints.

---

## 3. Create Pages

**POST**

```text
/documents/{document_id}/pages
```

Creates page records for an uploaded PDF.

### What it does

- Reads the uploaded PDF.
- Splits the PDF into individual pages.
- Converts pages into PNG images.
- Stores page information in PostgreSQL.

### Path parameter

```text
document_id
```

### Example response

```json
{
  "document_id": "...",
  "status": "PAGES_CREATED"
}
```

---

## 4. Extract Markdown

**POST**

```text
/documents/{document_id}/markdown
```

Generates markdown from the page images using Ollama Vision.

### What it does

- Reads the generated page images.
- Sends each page image to Ollama.
- Uses the markdown extraction prompt.
- Stores the generated markdown for the pages.

### Path parameter

```text
document_id
```

### Example response

```json
{
  "document_id": "...",
  "status": "MARKDOWN_EXTRACTED"
}
```

---

## 5. Create Document Type

**POST**

```text
/document-types
```

Creates a document type that can later be used during classification.

Examples:

```text
Invoice
Purchase Order
Receipt
Annual Report
```

### Parameters

```text
document_type_name
document_type_description
```

---

## 6. View Document Types

**GET**

```text
/document-types
```

Returns all configured document types.

The available document types are used by the document classification process.

---

## 7. Classify Document

**POST**

```text
/documents/{document_id}/classification
```

Classifies a document using the markdown extracted from its pages.

### What it does

- Reads the document's page markdown.
- Retrieves the configured document types.
- Sends the classification prompt to Ollama.
- Determines the predicted document type.

### Path parameter

```text
document_id
```

### Returns

The predicted document type.

---

## 8. Create Prompt

**POST**

```text
/prompts
```

Creates an extraction prompt.

Each prompt is associated with a document type.

### Parameters

```text
prompt_name
prompt
document_type_id
```

The prompt determines what structured information should be extracted from a classified document.

---

## 9. View Prompts

**GET**

```text
/prompts
```

Returns all configured extraction prompts.

These prompts are later used during structured data extraction.

---

## 10. Update Prompt

**PATCH**

```text
/prompts/{prompt_id}
```

Updates an existing prompt.

The request body can contain:

```json
{
  "prompt": "Updated extraction instructions",
  "document_type_id": "..."
}
```

Both fields are optional.

This allows the prompt text and/or its associated document type to be updated.

---

## 11. Extract Structured Data

**POST**

```text
/documents/{document_id}/extracted-data
```

This is the final AI processing stage.

### What it does

- Reads the markdown generated for the document.
- Retrieves the extraction prompt associated with the classified document type.
- Loads the document extraction rules.
- Sends the prompt and markdown to Ollama.
- Extracts structured JSON.
- Stores the extracted JSON in PostgreSQL.

### Path parameter

```text
document_id
```

### Returns

The extracted structured JSON data.

---

# Typical Workflow

## Initial Configuration

Document types and prompts need to be configured before processing documents.

```text
Create Document Type
        │
        ▼
Create Extraction Prompt
        │
        ▼
Ready for Document Processing
```

These configurations can then be reused for multiple documents.

---

## Document Processing

For a document, the processing sequence is:

```text
1. Upload Document
        ↓
2. Create Pages
        ↓
3. Extract Markdown
        ↓
4. Classify Document
        ↓
5. Extract Structured Data
```

The document ID returned during upload is used throughout the processing pipeline.

---

# Example Processing Flow

For example, an invoice can be processed as follows:

```text
Invoice PDF
    │
    ▼
Upload
    │
    ▼
Document stored in PostgreSQL
    │
    ▼
Pages created
    │
    ▼
Page images generated
    │
    ▼
Ollama Vision
    │
    ▼
Markdown generated
    │
    ▼
Document Classification
    │
    ▼
"INVOICE"
    │
    ▼
Invoice Extraction Prompt
    │
    ▼
Ollama Structured Extraction
    │
    ▼
JSON
    │
    ▼
Stored in PostgreSQL
```

---

# Project Documentation

Additional project documentation is available under `docs/`.

- `docs/Purpose.md` — Why I started this project.
- `docs/PlannedSolution.md` — The approach I planned before implementation.
- `docs/Architecture.md` — Overview of how the application is organized.

The `docs/Images/` directory contains screenshots demonstrating the application's workflow and API usage.

---

# Database Migrations

Alembic is used to manage database schema changes.

To apply all migrations:

```bash
alembic upgrade head
```

Migration files are stored under:

```text
alembic/versions/
```

---

# Environment and Secrets

The following files are intentionally excluded from version control:

```text
.env
.env.docker
```

They may contain credentials or environment-specific configuration.

The repository contains:

```text
.env.example
```

which can be used as a starting point when configuring the project.

No database passwords, API keys, or other secrets should be committed to the repository.

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
- Storing extracted JSON in PostgreSQL.
- Running the FastAPI application inside Docker.
- Connecting the Dockerized application to external PostgreSQL and Ollama services through environment-based configuration.

---

# Why I Built This

I built this project as a personal implementation exercise to understand the architecture and engineering considerations behind an AI-powered document processing system.

Rather than only calling an LLM API, the project focuses on the complete workflow:

```text
Document Ingestion
       ↓
PDF Processing
       ↓
Page Rendering
       ↓
Vision-based Markdown Extraction
       ↓
Document Classification
       ↓
Prompt-driven Extraction
       ↓
Structured JSON
       ↓
Database Persistence
```

The goal is to understand how these individual components work together to form a reusable Intelligent Document Processing pipeline.

---

# Thank You

If you took the time to explore this project, thank you.

I built this project to learn, experiment, and gain a deeper understanding of AI-powered document processing.

If you have suggestions, ideas, or feedback, I'd be happy to hear them.