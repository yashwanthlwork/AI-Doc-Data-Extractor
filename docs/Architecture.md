# Architecture

## Overview

I wanted to keep this project simple and easy to understand.

Instead of writing all the logic in one place, I divided the application into small services. Each service has one job. When its work is completed, it passes the result to the next service in the pipeline.

This makes the code easier to read, test, and maintain. It also allows me to modify one part of the application without affecting the entire project.

The application follows a simple flow:

```text
Client
   │
   ▼
FastAPI
   │
   ▼
Service
   │
   ▼
Database / Ollama
```

---

# Project Structure

The project is organized into a few folders, each with a specific purpose.

```text
app/
│
├── Configuration/
├── DBModels/
├── Prompts/
├── Services/
└── main.py
```

### Configuration

Contains the database configuration and session management.

---

### DBModels

Contains the SQLAlchemy models used to create and access the database tables.

Examples:

- Document
- Page
- DocumentType
- Prompt

---

### Prompts

Contains the prompt templates used by the AI model.

Instead of writing long prompts inside the Python code, they are stored as separate text files so they are easier to manage and update.

---

### Services

This is where most of the application logic lives.

Each service performs one specific task.

---

### main.py

This is the entry point of the application.

It exposes the REST APIs and calls the required service based on the user's request.

---

# How a Document Moves Through the System

Whenever a document is uploaded, it goes through a series of steps.

```text
Upload PDF
      │
      ▼
Save Document
      │
      ▼
Split PDF into Pages
      │
      ▼
Create PNG for Each Page
      │
      ▼
Extract Markdown
      │
      ▼
Classify Document
      │
      ▼
Load Prompt
      │
      ▼
Extract Structured Data
      │
      ▼
Save JSON
```

Each step depends on the output of the previous step.

For example, the document cannot be classified until markdown has been generated, and structured data cannot be extracted until the document type is known.

---

# Services

## DocumentService

This is the first service in the pipeline.

Its job is simple.

It accepts the uploaded PDF and stores it in the database along with some basic document information.

At this stage, nothing is extracted from the document.

---

## PageService

Once the document is uploaded, the PageService reads the PDF and splits it into individual pages.

Each page is converted into a PNG image.

After that, every page image is sent to Ollama to generate markdown.

Both the page image and the generated markdown are stored in the database because they are reused in later steps.

---

## DocumentTypeService

This service maintains the list of document types supported by the application.

Examples include:

- Invoice
- Purchase Order
- Receipt

The classification process uses this list to identify the type of the uploaded document.

---

## PromptService

Different document types require different extraction instructions.

This service stores the extraction prompt for each document type.

Once a document is classified, the application retrieves the corresponding prompt from this service.

---

## DocumentClassificationService

This service identifies the type of the uploaded document.

It reads the markdown generated for each page and asks the AI model to predict the document type.

Once all pages are processed, the final document type is stored in the database.

---

## DocumentDataExtractionService

This is the final processing step.

It retrieves:

- the document,
- its pages,
- the markdown,
- and the extraction prompt.

It then sends the information to Ollama to extract structured data.

The extracted JSON is finally stored in the Documents table.

---

## OllamaService

This service is the only place where the application interacts with the AI model.

Instead of calling Ollama from multiple places, every AI-related operation goes through this service.

Currently, it is responsible for:

- Markdown extraction
- Document classification
- Structured data extraction

Keeping all AI code in one place makes the rest of the application cleaner and easier to maintain.

---

# Database

The application currently uses four main tables.

| Table | Purpose |
|--------|---------|
| Documents | Stores uploaded PDFs, document information, processing status, and extracted JSON. |
| Pages | Stores individual page images and their markdown. |
| DocumentTypes | Stores the list of supported document types. |
| Prompts | Stores the extraction prompt for each document type. |

---

# Why Store Intermediate Results?

Instead of generating everything every time, the application stores the output after each major step.

For example:

- The uploaded PDF is stored.
- The generated page images are stored.
- The markdown is stored.
- The extracted JSON is stored.

This makes it easier to continue processing without repeating previous work.

It also makes debugging much easier because every stage of the document can be inspected independently.

---

# Why Separate Everything into Services?

During development, I wanted each service to solve one problem.

For example:

- DocumentService only handles document upload.
- PageService only works with document pages.
- PromptService only manages prompts.
- DocumentClassificationService only identifies the document type.
- DocumentDataExtractionService only extracts structured data.

This keeps the code organized and prevents one file from becoming too large or handling unrelated tasks.

---

# Summary

The architecture is intentionally simple.

A document enters through the FastAPI API, moves through a series of services, and each service performs one small task before passing the result to the next step.

The database stores both intermediate and final results, while the OllamaService handles all AI-related operations.

This approach made the project easier to build, easier to debug, and easier to extend as new features were added.