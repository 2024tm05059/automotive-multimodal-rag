# 🚗 Automotive Intelligence — Multimodal RAG System

> **Student:** Pradeep Nimesh | **ID:** 2024TM05059
> **Course:** Multimodal Retrieval-Augmented Generation Bootcamp — BITS Pilani WILP

---

## Problem Statement

### Domain Identification

This system operates in the **automotive engineering & vehicle systems domain**, focusing on technical manuals and documentation such as braking systems, engine components, and mechanical subsystems.

---

### Problem Description

Modern automotive systems are documented using multiple formats:

* **Technical manuals (PDFs):** Contain explanations of systems like braking, suspension, and transmission.
* **Engineering diagrams (images):** Show internal components, layouts, and working principles.
* **Tables & structured data:** Specifications, component lists, and performance parameters.

The challenge is:

> When a user asks:
> **“Explain the braking system and its components from the diagram”**
>
> The answer is spread across:

* Text explanations
* Diagrams
* Image-based descriptions

Traditional search systems cannot combine these modalities effectively.

---

### Why This Problem Is Unique

1. **Multimodal Understanding:** Requires combining text + images.
2. **Technical Context:** Engineering diagrams need interpretation.
3. **Scattered Knowledge:** Information split across pages and formats.
4. **Semantic Queries:** “Working of braking system” ≠ exact text match.
5. **Educational Use:** Needs clear and structured answers.

---

### Why RAG Is the Right Approach

| Approach         | Limitation                                    |
| ---------------- | --------------------------------------------- |
| Keyword Search   | Cannot understand diagrams                    |
| Manual Reading   | Time-consuming                                |
| Fine-tuning      | Expensive and static                          |
| **RAG (Chosen)** | Retrieves relevant chunks + generates answers |

---

### Expected Outcomes

* Explain automotive systems (e.g., braking system)
* Interpret diagrams
* Retrieve relevant sections quickly
* Combine image + text understanding
* Provide structured answers with sources

---

## Architecture Overview

```
┌──────────────────────────────────────────────┐
│                INGESTION                     │
│                                              │
│  PDF Upload → Parser (PyMuPDF)               │
│        │                                     │
│        ├── Text Chunks                       │
│        ├── Images → Gemini Vision Summary    │
│        │                                     │
│        ▼                                     │
│   Sentence Transformer Embeddings            │
│        ▼                                     │
│        ChromaDB Vector Store                 │
└──────────────────────────────────────────────┘

┌──────────────────────────────────────────────┐
│                 QUERY                        │
│                                              │
│  Question → Embed → Vector Search (Top-K)    │
│                         │                    │
│                         ▼                    │
│              Retrieve Relevant Chunks        │
│                         ▼                    │
│              Return Combined Answer          │
└──────────────────────────────────────────────┘
```
<img width="1804" height="1911" alt="mermaid-diagram" src="https://github.com/user-attachments/assets/cd09d899-a3fb-46ad-9e4c-c6fc33cda9c7" />


---

## Technology Choices

| Component    | Choice             | Reason                |
| ------------ | ------------------ | --------------------- |
| PDF Parser   | PyMuPDF            | Handles text + images |
| Embeddings   | `all-MiniLM-L6-v2` | Fast + local          |
| Vector DB    | ChromaDB           | Easy filtering        |
| Vision Model | Gemini API         | Image summarization   |
| Backend      | FastAPI            | Simple + fast         |

---

## Setup Instructions

### 1️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 2️⃣ Set API Key

```powershell
$env:GEMINI_API_KEY="AIzaSyBdCbowzCCdu36vaPasJSZndoyg0plfbjM"
```

---

### 3️⃣ Run Server

```bash
uvicorn main:app --reload
```

---

### 4️⃣ Open API Docs

```
http://127.0.0.1:8000/docs
```

---

## API Documentation

---

### 🔹 GET `/health`

```json
{
  "status": "ok"
}
```

---

### 🔹 POST `/ingest`

Upload PDF

**Response:**

```json
{
  "filename": "braking system.pdf",
  "text_chunks": 12,
  "image_chunks": 17,
  "total_chunks": 29
}
```

---

### 🔹 POST `/query`

```text
/query?q=Explain braking system
```

**Response:**

```json
{
  "answer": "The braking system works by...",
  "sources": [
    {
      "page": 2,
      "type": "text"
    },
    {
      "page": 5,
      "type": "image"
    }
  ]
}
```

---

### 🔹 GET `/documents`

```json
{
  "documents": ["braking system.pdf"],
  "total": 1
}
```

---

### 🔹 DELETE `/delete`

```json
{
  "filename": "braking system.pdf",
  "chunks_removed": 29
}
```

---

## Screenshots

| # | Screenshot | Description             |
| - | ---------- | ----------------------- |
| 1 | Swagger UI | <img width="1844" height="695" alt="Screenshot 2026-04-05 201753" src="https://github.com/user-attachments/assets/3602fdcd-2c61-47d5-9cf4-82a124a43ee6" />
            |
| 2 | Ingest     | <img width="1789" height="581" alt="Screenshot 2026-04-05 204247" src="https://github.com/user-attachments/assets/acce2e73-2650-47de-bfc6-4545e15389e7" />
             |
| 3 | Query      |<img width="1793" height="724" alt="Screenshot 2026-04-05 221533" src="https://github.com/user-attachments/assets/fc1a70ed-a53e-4271-9042-331933f80c28" />
         |
| 4 | Images     | Extracted images folder |

---

## Limitations & Future Work

### Current Limitations

1. No OCR support (scanned PDFs not handled)
2. Basic answer generation (no advanced LLM reasoning)
3. No authentication
4. Works only for English PDFs

---

### Future Improvements

* Add OCR support
* Improve answer generation using LLM
* Add frontend UI
* Support multiple documents
* Add better ranking

---

## Repository Structure

```
automotive-multimodal-rag/
├── main.py
├── requirements.txt
├── README.md
├── .env.example
├── src/
│   ├── api/
│   ├── ingestion/
│   ├── retrieval/
│   ├── models/
├── sample_documents/
├── screenshots/
```

---

## Final Status

*  ✅ PDF ingestion working
*  ✅ Image extraction working
*  ✅ Image summarization working
*  ✅ Vector search working
*  ✅ Query system working

---

## 🎓 Conclusion

This project successfully demonstrates a **Multimodal RAG system** capable of:

* Understanding automotive documents
* Combining text and image knowledge
* Providing meaningful answers

---

**BITS Pilani • WILP • Automotive Multimodal RAG Project** **Pradeep Nimesh 2024tm05059**
