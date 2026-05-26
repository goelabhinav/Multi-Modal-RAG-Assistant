# Multi-Modal RAG Assistant — Build Instructions

You are a senior AI engineer helping build a production-grade Multi-Modal RAG Assistant for QA and incident investigation.

## Objective

Build an AI assistant capable of:

* understanding screenshots
* parsing logs
* reading PDFs
* analyzing UI failures
* retrieving historical incidents
* generating root cause analysis reports

The assistant should use:

* Retrieval-Augmented Generation (RAG)
* multimodal understanding
* vector embeddings
* AI agents
* model deployment best practices

---

# Primary Use Case

Users upload:

* failed UI screenshots
* CI/CD logs
* Jira tickets
* PDFs
* accessibility reports

The assistant should:

1. extract information
2. create embeddings
3. retrieve relevant historical data
4. analyze probable root causes
5. generate AI summaries and recommendations

---

# Technical Requirements

## Backend

* Python
* FastAPI

## Frontend

* React

## AI Framework

* LangChain

## Vector Database

* Qdrant

## LLM Support

Support:

* OpenAI GPT models
* Claude models
* Ollama local models

Use provider abstraction.

---

# Required Features

## Document Ingestion

Support:

* PDF
* PNG/JPG screenshots
* TXT logs
* JSON reports

---

## OCR & Vision

Implement:

* OCR extraction
* screenshot analysis
* multimodal processing

Use:

* Tesseract OR GPT Vision APIs

---

## RAG Pipeline

Implement:

1. document chunking
2. embedding generation
3. vector indexing
4. semantic retrieval
5. reranking
6. prompt augmentation

---

## Embeddings

Support:

* text embeddings
* image embeddings

Prefer:

* sentence-transformers
* OpenAI embeddings

---

## AI Agents

Create separate agents for:

* screenshot analysis
* log analysis
* incident correlation
* root cause analysis
* report generation

Use LangGraph if possible.

---

# UI Requirements

Provide:

* chat interface
* drag-and-drop uploads
* citations
* confidence scores
* retrieval sources
* dark mode support

---

# Deployment Requirements

Use:

* Docker
* docker-compose

Provide:

* backend Dockerfile
* frontend Dockerfile
* Qdrant setup

---

# Observability

Implement:

* logging
* tracing
* token usage monitoring
* latency tracking

Optional:

* LangSmith integration

---

# Project Structure

Create:

* backend/
* frontend/
* agents/
* rag/
* embeddings/
* ingestion/
* vectorstore/
* deployment/
* tests/

---

# API Endpoints

Include:

* upload document
* query assistant
* retrieve sources
* incident summary
* health check

---

# Evaluation

Implement:

* retrieval relevance scoring
* hallucination detection
* groundedness evaluation

---

# Security

Implement:

* API key management
* environment variable handling
* upload validation
* file size limits

---

# Deliverables

Generate:

* complete architecture
* backend implementation
* frontend implementation
* Docker deployment
* README
* setup guide
* sample test data
* evaluation scripts

Focus on clean architecture, modularity, scalability, and enterprise-quality implementation.


USE the cheap mvp version
| Component           | Cost |
| ------------------- | ---- |
| Ollama local models | Free |
| Qdrant local        | Free |
| Streamlit frontend  | Free |
| Docker              | Free |
| SQLite/Postgres     | Free |
| Local embeddings    | Free |
