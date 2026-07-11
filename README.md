# Preclinical Study RAG

An end-to-end Retrieval-Augmented Generation (RAG) application that answers questions over **preclinical toxicology studies** and **regulatory guidelines** using semantic search.

The project demonstrates the core building blocks of a RAG system:

- PDF ingestion
- Text chunking
- Embedding generation
- Vector database (ChromaDB)
- Semantic retrieval
- LLM-powered answer generation

The objective of this project was **to understand how modern RAG systems work** by building one from scratch with minimal abstractions.

---

## Motivation

Researchers frequently need to answer questions such as:

- How are 28-day oral toxicity studies typically designed?
- Which animal models are commonly used?
- What endpoints are measured across different studies?
- How do published studies compare with OECD/FDA guidance?

Instead of manually reading multiple papers, this application retrieves the most relevant document chunks and uses an LLM to generate an evidence-based answer.

---

## Architecture

```
                PDFs
                  │
                  ▼
          ingest.py
                  │
                  ▼
          chunks.json
                  │
                  ▼
        vectorise.py
                  │
                  ▼
        Chroma Vector DB
                  │
                  ▼
            chat.py
                  │
                  ▼
      Semantic Retrieval
                  │
                  ▼
             Local / OpenAI LLM
                  │
                  ▼
            Grounded Answer
```

---

## Tech Stack

| Component | Technology |
|----------|------------|
| Language | Python 3.12 |
| PDF Parsing | PyMuPDF |
| Embeddings | sentence-transformers (`all-MiniLM-L6-v2`) |
| Vector Database | ChromaDB |
| LLM | Ollama (Gemma/Qwen) or OpenAI |
| Retrieval | Cosine Similarity Search |

---

## Project Structure

```
preclinical-study-rag/

├── data/
├── output/
├── chroma_db/
│
├── ingest.py
├── vectorise.py
├── chat.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Setup

Create a virtual environment.

```bash
python3.12 -m venv .venv
```

Activate it.

### macOS / Linux

```bash
source .venv/bin/activate
```

### Windows

```bash
.venv\Scripts\activate
```

Install dependencies.

```bash
pip install -r requirements.txt
```

---

## Prepare Dataset

Place all PDFs inside the `data/` directory.

Example:

```
data/

OECD407.pdf
ICH_M3.pdf
study1.pdf
study2.pdf
...
```

The repository intentionally does **not** include PDFs because many scientific papers are copyrighted.

---

## Step 1 — Extract and Chunk PDFs

```bash
python ingest.py
```

This generates:

```
output/chunks.json
```

Each chunk contains:

- document name
- chunk id
- character offsets
- chunk text

---

## Step 2 — Create Vector Database

```bash
python vectorise.py
```

This:

- generates embeddings
- stores them in ChromaDB
- creates the local vector database

---

## Step 3 — Ask Questions

```bash
python chat.py
```

Example:

```
Ask a question:

What biomarkers are commonly measured in repeated-dose toxicity studies?
```

The application first displays the retrieved chunks before generating the final answer.

---

## Example Questions

- Compare study designs across the retrieved studies.

- What biomarkers are commonly measured?

- Which animal species are most frequently used?

- Which organs are evaluated during repeated-dose toxicity studies?

- Summarize the OECD recommendations for 28-day oral toxicity studies.

- Compare the dose ranges used across different studies.

- Which studies reported liver toxicity?

- What endpoints are consistently measured?

---

## Sample Output

```
========== Retrieved Chunks ==========

1. OECD407.pdf
Distance : 0.61

...

2. Study_A.pdf
Distance : 0.63

...

========== Answer ==========

Repeated-dose oral toxicity studies commonly evaluate body weight,
food consumption, hematology, clinical chemistry and histopathology.

These endpoints are consistently described across OECD 407 and
multiple published studies.
```

---

## Current Limitations

This project intentionally keeps the implementation simple.

Current limitations include:

- Fixed-size character chunking
- No reranking
- No metadata filtering
- No hybrid search
- Small document corpus
- Basic prompting

These trade-offs were made to keep the MVP focused on understanding the fundamentals of RAG.

---

## Future Improvements

- Paragraph-aware chunking
- Metadata extraction (species, dose, duration, route)
- Hybrid search (keyword + vector)
- Cross-encoder reranking
- Citation-aware responses
- Web interface
- Support for additional scientific domains

---

## What I Learned

Building this project provided hands-on experience with:

- semantic embeddings
- vector databases
- document chunking strategies
- retrieval tuning
- prompt grounding
- practical RAG system design

One important observation during development was that retrieval quality depended significantly on the **Top-K** parameter. Increasing the number of retrieved chunks improved recall for broader research questions while maintaining answer quality.

---

## License

MIT
