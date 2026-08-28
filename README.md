# 🛡️ AI-Enabled Multi-Document Search & Query System

> **A lightweight, explainable document-intelligence system for searching and querying organisational documents using natural language.**

## 📌 Overview

Organisations often maintain large collections of documents containing interconnected information about procurement, budgets, projects, assets, infrastructure and operational activities.

Finding a specific piece of information manually can require opening multiple documents, searching for keywords, comparing different sections and verifying the original source.

This project addresses that problem by providing a **unified multi-document search and query interface**.

Users can upload multiple organisational documents and ask questions using natural language. The system processes the uploaded documents, extracts and cleans their text, divides the content into searchable passages, represents the passages using TF-IDF, and retrieves the most relevant information using cosine similarity.

The application also preserves **document and page-level metadata**, allowing users to identify and verify the source behind the retrieved information.

The result is a lightweight prototype for **explainable and traceable document intelligence**.

---

# 🎯 Problem Statement

The objective of the project is to develop a prototype application capable of making a collection of organisational documents:

- Searchable
- Understandable
- Queryable using natural language
- Useful for decision-making
- Traceable back to the original source

The system is designed around five core capabilities:

1. **Multiple Document Input**
2. **Document Processing**
3. **Natural-Language Search**
4. **AI-Based Question Answering**
5. **Source Identification**

The documents can contain related information distributed across multiple files. Therefore, the system is designed to search the **complete uploaded document collection** rather than forcing the user to manually inspect each document individually.

---

# 💡 Why This Project?

Traditional document search generally depends on exact keyword matching.

For example, if a user searches for:

```text
pending server procurement
```

a conventional search engine may only return documents containing those exact words.

However, organisational information may be expressed in different ways:

```text
server procurement pending
additional server requirement
technical evaluation pending
hardware acquisition
server requirement under review
```

A document-intelligence system should therefore provide a more useful retrieval mechanism and preserve the evidence behind the result.

This project focuses on two important principles:

### 🔎 Retrieval

Find the most relevant information from the document collection.

### 📚 Traceability

Show the user where that information came from.

---

# 🏗️ High-Level Architecture

```text
                         USER
                           │
                           ▼
                ┌────────────────────┐
                │   Streamlit Web UI  │
                └──────────┬─────────┘
                           │
                           ▼
                ┌────────────────────┐
                │ Multiple Document  │
                │      Upload        │
                └──────────┬─────────┘
                           │
                           ▼
                ┌────────────────────┐
                │ Text Extraction    │
                │                    │
                │ PDF → PyMuPDF      │
                │ DOCX → python-docx │
                │ TXT → Text Reader  │
                └──────────┬─────────┘
                           │
                           ▼
                ┌────────────────────┐
                │   Text Cleaning    │
                └──────────┬─────────┘
                           │
                           ▼
                ┌────────────────────┐
                │ Document Chunking  │
                └──────────┬─────────┘
                           │
                           ▼
                ┌────────────────────┐
                │ TF-IDF Vectorizer  │
                └──────────┬─────────┘
                           │
                           ▼
                ┌────────────────────┐
                │ Searchable Matrix  │
                └──────────┬─────────┘
                           │
                           │
                    USER QUESTION
                           │
                           ▼
                ┌────────────────────┐
                │ Query Vectorisation│
                └──────────┬─────────┘
                           │
                           ▼
                ┌────────────────────┐
                │ Cosine Similarity  │
                └──────────┬─────────┘
                           │
                           ▼
                ┌────────────────────┐
                │ Relevant Passages  │
                └──────────┬─────────┘
                           │
                  ┌────────┴────────┐
                  ▼                 ▼
          ┌──────────────┐   ┌───────────────┐
          │   Grounded   │   │    Source     │
          │    Answer    │   │ Identification│
          └──────────────┘   └───────────────┘
                                  │
                                  ▼
                         Document + Page
                         + Passage + Score
```

---

# 🛠️ Technology Stack

| Technology | Role in the Project |
|---|---|
| **Python** | Core application and processing logic |
| **Streamlit** | Interactive web interface |
| **PyMuPDF** | Page-level PDF text extraction |
| **python-docx** | DOCX document processing |
| **Scikit-learn** | TF-IDF vectorisation and cosine similarity |
| **NumPy** | Numerical operations |
| **OpenAI API** | Optional answer-generation layer |

---

# 🔄 End-to-End Workflow

## 1️⃣ Multiple Document Upload

The user can upload multiple documents through the Streamlit interface.

Supported formats:

```text
PDF
TXT
DOCX
```

The system treats the uploaded files as a single searchable document collection.

---

## 2️⃣ Document Processing

When the user clicks:

```text
⚙️ Process Documents
```

the application processes every uploaded file.

The appropriate extraction method is selected based on the file type.

### PDF

PDF text is extracted using:

```text
PyMuPDF
```

The document is processed page by page.

### DOCX

Text is extracted using:

```text
python-docx
```

### TXT

Plain-text files are read directly.

---

# 🧹 3️⃣ Text Cleaning

Raw extracted document text can contain:

- Line breaks
- Excessive whitespace
- Formatting artefacts
- Inconsistent spacing

The application performs basic cleaning before indexing.

For example:

```text
Raw text:

Project C
       
Charlie Centre

Pending
Technical Evaluation
```

becomes a cleaner searchable representation:

```text
Project C Charlie Centre Pending Technical Evaluation
```

This makes downstream retrieval more consistent.

---

# 🧩 4️⃣ Document Chunking

Instead of treating an entire document as one large block of information, the application divides larger text into smaller searchable passages.

Conceptually:

```text
Document
   │
   ├── Chunk 1
   ├── Chunk 2
   ├── Chunk 3
   └── Chunk 4
```

Each chunk retains metadata:

```python
{
    "text": "...",
    "document": "example.pdf",
    "page": 1
}
```

This metadata is important because retrieval should not lose the original location of the information.

---

# 📊 5️⃣ TF-IDF Representation

The current prototype uses:

**TF-IDF — Term Frequency-Inverse Document Frequency**

TF-IDF converts textual passages into numerical vectors.

It considers two main ideas:

### Term Frequency

How frequently a term appears in a passage.

### Inverse Document Frequency

How distinctive that term is across the document collection.

Conceptually:

```text
TF-IDF = Term Frequency × Inverse Document Frequency
```

The resulting vectors allow textual passages and user queries to be compared mathematically.

---

# 🔎 6️⃣ Natural-Language Query

The user can ask questions in normal language.

For example:

```text
Which entities have pending server procurement
and what amount was allocated?
```

The question is converted into the same TF-IDF representation used for the document passages.

---

# 📐 7️⃣ Cosine Similarity Retrieval

The system compares the query vector with the vectors representing the document chunks.

The similarity calculation uses:

**Cosine Similarity**

Conceptually:

```text
             Query
               │
               ▼
         Query Vector
               │
               │
       ┌───────┴────────┐
       ▼                ▼
 Document Chunk 1   Document Chunk 2
       │                │
       ▼                ▼
   Similarity        Similarity
       │                │
       └───────┬────────┘
               ▼
        Ranked Results
```

The highest-scoring passages are treated as the most relevant results.

---

# 🤖 8️⃣ Grounded Answer Layer

The system uses the retrieved passages as the evidence for presenting an answer.

Instead of requiring the user to inspect every document manually, the application surfaces the information that is most relevant to the question.

The current implementation focuses on a **lightweight grounded retrieval/answering approach**.

An optional OpenAI API integration is also supported as an answer-generation layer.

For production deployment, this component could be replaced by an approved enterprise or local LLM.

---

# 📚 9️⃣ Source Identification

Source traceability is one of the central design decisions of the application.

Every retrieved passage maintains:

```text
📄 Document Name
📑 Page Number
📝 Retrieved Passage
📊 Relevance Score
```

For example:

```text
Document:
Server_Procurement_Proposal.pdf

Page:
1

Relevance:
87.4%

Passage:
...
```

This allows a user to go back to the original document and verify the information.

---

# ⭐ Key Features

## 📂 Multi-Document Input

Upload multiple documents and treat them as a single searchable knowledge collection.

---

## 🔎 Natural-Language Search

Users can ask questions without manually searching for exact phrases.

Example:

```text
What is the procurement status of Project C?
```

---

## 📊 Similarity-Based Retrieval

Relevant document passages are ranked using cosine similarity.

---

## 📚 Source Traceability

Every retrieved result preserves its original document and page information.

---

## 📈 Relevance Scoring

The interface exposes the similarity score associated with retrieved passages.

This helps users understand which results were ranked more strongly.

> The relevance score is a retrieval similarity measure and should not be interpreted as a guaranteed factual confidence score.

---

## 🗂️ Document-Wise Retrieval

The application shows which documents contributed relevant passages to a query.

This provides visibility into cross-document retrieval.

---

## 📄 Multiple File Formats

The current interface supports:

```text
PDF
TXT
DOCX
```

---

# 🔍 Example Use Case

Consider an organisation managing several related documents:

```text
Budget Allocation Report
        │
        ├──────────────┐
        │              │
        ▼              ▼
Procurement       Project Status
Status Report         Report
        │              │
        └──────┬───────┘
               │
               ▼
       Server Procurement
             Proposal
               │
               ▼
        Digital Asset
            Register
```

Information about a single entity can therefore be distributed across different documents.

A user can ask:

```text
Which entities have pending server procurement
and what amount was allocated?
```

Instead of manually opening each file, the system retrieves the relevant passages from the document collection.

---

# 🧪 Example Queries

### Query 1

```text
Which entities have pending server procurement and what amount was allocated?
```

### Query 2

```text
What is the procurement status of Project C?
```

### Query 3

```text
What is the current asset situation at Charlie Centre?
```

### Query 4

```text
Which projects are currently under procurement?
```

### Query 5

```text
Which documents contain information related to Project C?
```

---

# 🖥️ Application Interface

The application contains four primary areas.

### 1. Document Management

```text
📂 Upload multiple documents
⚙️ Process Documents
```

### 2. Natural-Language Query

```text
🔍 Ask a Natural-Language Question
```

### 3. Answer

```text
🤖 Grounded Answer
```

### 4. Evidence

```text
📚 Source Identification
📊 Document-wise Search Results
```

This provides a complete flow from ingestion to retrieval and verification.

---

# 🧠 Why This Architecture?

A key design decision was to avoid unnecessarily training a machine-learning model from scratch.

The problem is primarily an **information retrieval problem over existing documents**.

Therefore, the architecture focuses on:

```text
Document Processing
        ↓
Representation
        ↓
Retrieval
        ↓
Evidence
        ↓
Answer
        ↓
Source Verification
```

This makes the prototype:

- Lightweight
- Fast
- Explainable
- Easy to modify
- Easy to extend

---

# ⚖️ Why TF-IDF?

TF-IDF was selected for the rapid prototype because it provides:

- Lightweight computation
- Fast indexing
- Easy implementation
- Interpretability
- No custom model training requirement

It is particularly suitable for demonstrating the complete retrieval pipeline within a limited development time.

However, TF-IDF is primarily lexical and therefore has limitations when semantically related concepts use very different terminology.

---

# 📐 Why Cosine Similarity?

Cosine similarity provides a simple way to compare the query representation with document representations.

A higher similarity indicates that the query and passage are more closely aligned in the vector space.

This allows the application to:

```text
Query
  ↓
Compare against all chunks
  ↓
Calculate similarity
  ↓
Rank results
  ↓
Return top relevant passages
```

---

# 🔐 Security Considerations

The application is designed as a prototype and should not be considered a production security architecture.

For deployment with sensitive organisational documents, additional security controls would be required.

## Authentication

Only authorised users should be able to access the system.

## Role-Based Access Control

Users should only be able to retrieve documents they are authorised to access.

Example:

```text
Administrator
     ↓
All Documents

Department A
     ↓
Department A Documents

Department B
     ↓
Department B Documents
```

## Encryption

Sensitive documents should be protected:

```text
At Rest
+
In Transit
```

## Audit Logging

A production system should record:

```text
User
Timestamp
Query
Documents Retrieved
Sources Used
Answer Generated
```

## Sensitive Data Protection

Sensitive organisational documents should not automatically be transmitted to external APIs.

For highly sensitive environments, an approved local or on-premise model can be considered.

## Prompt Injection Protection

Documents should be treated as **untrusted data**.

Instructions contained inside an uploaded document should not automatically become instructions for the AI model.

---

# ⚠️ Current Limitations

The current version is intentionally lightweight.

### 1. Lexical Retrieval

TF-IDF is less semantically powerful than transformer-based embeddings.

### 2. Scanned Documents

Image-only PDFs require OCR before text extraction.

### 3. Large-Scale Storage

The current prototype uses in-memory processing and is not designed for millions of documents.

### 4. Retrieval Confidence

Similarity scores represent retrieval relevance and do not guarantee factual correctness.

### 5. Enterprise Security

Authentication, RBAC, encryption infrastructure and audit systems would need to be added for production deployment.

### 6. Answer Generation

The local prototype prioritises retrieval and evidence presentation. A production system would use a stronger controlled generation layer.

---

# 🚀 Future Improvements

The architecture is intentionally modular, allowing several upgrades.

## 🧠 Semantic Embeddings

Replace TF-IDF with models such as:

```text
Sentence Transformers
```

This would provide deeper semantic retrieval.

For example:

```text
"server procurement pending"
```

could potentially retrieve:

```text
"additional hardware requirement awaiting approval"
```

even when the exact keywords differ.

---

## ⚡ Vector Database

The retrieval layer can be upgraded to:

```text
Sentence Embeddings
        ↓
FAISS
        ↓
Vector Database
```

Potential production choices include a persistent vector database with metadata filtering.

---

## 🤖 Local / Enterprise LLM

The retrieval layer can be connected to an approved LLM:

```text
User Question
      ↓
Retriever
      ↓
Relevant Context
      ↓
LLM
      ↓
Grounded Answer
      ↓
Source References
```

For sensitive deployments, a local/on-premise LLM can reduce exposure of organisational data.

---

## 🖨️ OCR

For scanned PDFs:

```text
Scanned PDF
     ↓
Image Extraction
     ↓
OCR
     ↓
Text
     ↓
Cleaning
     ↓
Chunking
     ↓
Indexing
```

---

## 💬 Conversational Follow-Up

The system can be extended from one-shot queries to conversations:

```text
User:
What is the status of Project C?

System:
Pending technical evaluation.

User:
Which entity is associated with it?

System:
Charlie Centre.

User:
What server requirement does it have?

System:
...
```

---

## 📚 Multi-Document Summarisation

Users could request:

```text
Summarise all procurement-related information.
```

The system would retrieve relevant passages across documents and produce a consolidated summary.

---

## ⚖️ Document Comparison

The system could compare two documents and identify:

- Common information
- Conflicting information
- Updated values
- Missing information
- Changes over time

---

## 🔦 Passage Highlighting

Relevant terms and sentences could be highlighted directly in the retrieved evidence.

---

## ♻️ Duplicate Detection

The ingestion pipeline can identify duplicate or near-duplicate documents before indexing.

---

## ➕ Incremental Indexing

Instead of rebuilding the complete index whenever a document is added:

```text
Existing Index
     +
New Document
     ↓
Process New Document
     ↓
Add New Vectors
```

This would significantly improve scalability.

---

# 📈 Production Architecture

For a real-world deployment, the Streamlit prototype could evolve into a service-oriented architecture:

```text
                         USERS
                           │
                           ▼
                    ┌─────────────┐
                    │ Web Frontend│
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │ API Gateway │
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
              ▼            ▼            ▼
        Authentication  Document     Query
                        Service      Service
                           │            │
                           ▼            │
                     Processing         │
                           │            │
                           ▼            ▼
                    ┌─────────────────────┐
                    │    Vector Database  │
                    └──────────┬──────────┘
                               │
                               ▼
                         Retrieval Layer
                               │
                               ▼
                         Approved LLM
                               │
                               ▼
                         Grounded Answer
                               │
                               ▼
                      Source Verification
```

This architecture would allow the application to support:

- Multiple users
- Persistent document storage
- Access control
- Scalable retrieval
- Background processing
- Model monitoring
- Audit trails

---

# 🧩 Project Structure

```text
AI-Document-Intelligence/
│
├── app.py
│
├── requirements.txt
│
├── README.md
│
├── .gitignore
│
└── documents/
    └── .gitkeep
```

Assessment documents are intentionally excluded from the repository.

---

# 💻 Installation

## Prerequisites

- Python 3.9+
- Git
- Windows / Linux / macOS

---

## 1. Clone the Repository

```bash
git clone YOUR_REPOSITORY_URL
cd AI-Document-Intelligence
```

---

## 2. Create a Virtual Environment

```bash
python -m venv venv
```

---

## 3. Activate the Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

---

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 5. Run the Application

```bash
python -m streamlit run app.py
```

The application will be available at:

```text
http://localhost:8501
```

---

# 📋 Usage

### Step 1 — Upload Documents

Upload one or more:

```text
PDF
TXT
DOCX
```

### Step 2 — Process Documents

Click:

```text
⚙️ Process Documents
```

### Step 3 — Ask a Question

Enter a natural-language query.

Example:

```text
What is the procurement status of Project C?
```

### Step 4 — Search

Click:

```text
🔎 Search & Answer
```

### Step 5 — Verify

Inspect:

```text
🤖 Grounded Answer

📚 Source Identification

📊 Document-wise Search Results
```

---

# 🧪 Testing Strategy

The application can be evaluated through several categories of queries.

## Direct Fact Retrieval

```text
What is the status of Project C?
```

## Entity-Based Retrieval

```text
What information is available about Charlie Centre?
```

## Cross-Document Retrieval

```text
Which entities have pending server procurement and what amount was allocated?
```

## Document-Specific Retrieval

```text
Which document contains information about server procurement?
```

## Unsupported Query

```text
What was the employee satisfaction score in 2026?
```

For information that is not present in the uploaded documents, the system should avoid inventing unsupported information.

---

# 🧠 Hallucination Mitigation

One of the major risks of AI-based document systems is **hallucination**.

Hallucination occurs when an AI system produces information that sounds plausible but is not supported by the available evidence.

For document intelligence applications, this can be particularly dangerous because users may assume that the generated answer came directly from the organisation's documents.

The architecture therefore emphasises:

```text
Question
   ↓
Retrieve Evidence
   ↓
Relevant Passages
   ↓
Answer
   ↓
Source Verification
```

Additional production safeguards would include:

- Restricting generation to retrieved context
- Requiring source references
- Rejecting insufficient evidence
- Human verification for critical decisions
- Audit logging
- Controlled model configuration
- Access-controlled document retrieval

---

# 📊 Explainability

The system is designed around the idea that an answer should be **verifiable**.

Instead of displaying only:

```text
Answer: Project C is pending.
```

the application also provides:

```text
Source:
Procurement_Status_Report.pdf

Page:
1

Relevant Passage:
...

Relevance:
...
```

This allows a human user to inspect the underlying evidence.

This is particularly useful for organisational decision-support systems where traceability is important.

---

# 🎯 Design Decisions

| Decision | Reason |
|---|---|
| **Streamlit** | Rapid development of an interactive prototype |
| **PyMuPDF** | Page-level PDF text extraction |
| **Chunking** | Enables passage-level retrieval |
| **TF-IDF** | Lightweight and interpretable text representation |
| **Cosine Similarity** | Simple relevance ranking |
| **Metadata Preservation** | Enables source traceability |
| **Local Retrieval** | Avoids unnecessary external data transfer |
| **Modular Architecture** | Makes future upgrades easier |

---

# 🔬 Current Architecture vs. Future Architecture

## Current Prototype

```text
Documents
    ↓
Text Extraction
    ↓
Cleaning
    ↓
Chunking
    ↓
TF-IDF
    ↓
Cosine Similarity
    ↓
Relevant Passages
    ↓
Grounded Answer
    ↓
Sources
```

## Future Production Version

```text
Documents
    ↓
OCR / Text Extraction
    ↓
Cleaning
    ↓
Intelligent Chunking
    ↓
Embedding Model
    ↓
Vector Database
    ↓
Hybrid Retrieval
    ↓
Reranking
    ↓
Approved / Local LLM
    ↓
Grounded Answer
    ↓
Citations + Evidence
```

The current architecture can therefore serve as the foundation for a more advanced RAG-style system.

---

# 📚 Concepts Demonstrated

This project demonstrates practical implementation of:

- Natural Language Processing
- Information Retrieval
- TF-IDF
- Vector Representation
- Cosine Similarity
- Text Preprocessing
- Document Chunking
- Metadata Management
- Retrieval-Based Question Answering
- Source Attribution
- Explainable AI
- Streamlit Application Development
- Document Intelligence
- AI Security Considerations

---

# 🏆 Project Highlights

### 🔹 Multi-Document Intelligence

Search across multiple organisational documents through one interface.

### 🔹 Natural-Language Interaction

Users can ask questions instead of constructing exact keyword searches.

### 🔹 Explainable Retrieval

Results include document, page and relevance information.

### 🔹 Modular Architecture

The retrieval layer can be upgraded without redesigning the entire application.

### 🔹 Privacy-Aware Design

The architecture can be extended toward local/on-premise AI for sensitive environments.

### 🔹 Production-Oriented Thinking

The project considers authentication, access control, audit logging, OCR, scalability and model upgrades as part of its future architecture.

---

# ⚠️ Important Note

This repository contains the **prototype implementation only**.

The assessment documents used during development are intentionally excluded from version control through `.gitignore`.

The current prototype should not be considered a production-ready enterprise document-management system. Production deployment would require additional security, scalability, reliability and access-control mechanisms.

---

# 🚀 Roadmap

- [x] Multi-document upload
- [x] PDF processing
- [x] TXT processing
- [x] DOCX processing
- [x] Text cleaning
- [x] Document chunking
- [x] TF-IDF representation
- [x] Cosine similarity retrieval
- [x] Source identification
- [x] Page-level references
- [x] Relevance scoring
- [x] Document-wise retrieval
- [ ] Sentence Transformer embeddings
- [ ] FAISS/vector database
- [ ] OCR pipeline
- [ ] Local LLM integration
- [ ] Conversational memory
- [ ] Document comparison
- [ ] Role-based access control
- [ ] Authentication
- [ ] Audit logging
- [ ] Production API architecture
- [ ] Incremental indexing

---

# 👨‍💻 Author

## Yashas Raina

**B.Tech — Artificial Intelligence & Machine Learning**

---

# ⭐ Final Takeaway

> **Upload → Process → Retrieve → Answer → Verify**

The primary goal of this project is not simply to build a chatbot.

It is to build an **explainable document-intelligence layer** that helps users discover relevant organisational information quickly while retaining the ability to verify where that information came from.

The current implementation provides a lightweight foundation using **TF-IDF and cosine similarity**, while its modular architecture allows future integration of **semantic embeddings, vector databases, local/enterprise LLMs, OCR, access control and production-scale infrastructure**.