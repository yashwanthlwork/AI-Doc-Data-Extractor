# Python AI Document Intelligence

## Overview

An Intelligent Document Processing (IDP) platform that extracts structured information from documents using local LLMs through Ollama.

## Features

- PDF Upload
- Page Generation
- Markdown Extraction
- Document Stage Tracking
- REST APIs
- PostgreSQL Storage

## Architecture

FastAPI
    │
    ▼
Services
    ├── DocumentService
    ├── PageService
    └── OllamaService
    │
    ▼
PostgreSQL

## Processing Pipeline

Upload Document
      │
      ▼
Store PDF
      │
      ▼
Create Pages
      │
      ▼
Extract Markdown
      │
      ▼
Store Markdown

## Current Project Status

✅ Upload Documents
✅ Create PNG Pages
✅ Extract Markdown using Ollama Vision
⬜ Document Classification
⬜ Prompt Management
⬜ Structured JSON Extraction
⬜ ETL Mapping

## Technology Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- PyMuPDF
- Ollama
- Gemma 3 Vision