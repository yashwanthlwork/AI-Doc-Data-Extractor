# Planned Solution

## Overview

The planned solution is to build a system that can automatically extract useful information from PDF documents using Artificial Intelligence.

Instead of manually reading documents and entering the information into another system, the user uploads a PDF, and the application processes it step by step to produce structured JSON data.

The solution is designed to be simple, configurable, and easy to extend for different document types.

---

# Solution Flow

The document is processed through the following steps:

1. Upload the PDF document.
2. Store the document in the database.
3. Split the PDF into individual pages.
4. Convert each page into markdown.
5. Identify the document type.
6. Load the extraction prompt for that document type.
7. Extract structured data from the document.
8. Store the extracted data.
9. Return the extracted JSON to the user.

---

# Planned Modules

The application is divided into small modules, where each module is responsible for one task.

### Document Management

Responsible for uploading documents and storing them in the database.

---

### Page Processing

Responsible for splitting a PDF into individual pages and generating page images.

---

### Markdown Extraction

Responsible for converting each page into markdown so that it can be understood by the language model.

---

### Document Type Management

Maintains the list of document types supported by the system.

Examples include:

- Invoice
- Purchase Order
- Receipt

---

### Prompt Management

Maintains the extraction prompt for each document type.

Each document type has its own prompt that tells the language model what information should be extracted.

---

### Document Classification

Determines the type of document by analyzing its content.

The identified document type is used to select the correct extraction prompt.

---

### Data Extraction

Extracts structured information from the document using the selected prompt.

The final output is returned as JSON.

---

# Configuration

The solution is designed so that some parts of the system can be configured without changing the source code.

These include:

- Supported document types.
- Extraction prompts for each document type.

This makes it easier to support new document types in the future.

---

# Expected Output

After processing is complete, the system returns structured JSON containing the extracted information from the document.

This JSON can be stored in a database or used by other applications.

---

# Summary

The planned solution is to create a simple document processing pipeline that accepts PDF documents, understands their contents using Artificial Intelligence, and converts the required information into structured JSON in an automated way.