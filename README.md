# 🛡️ AI-Enabled Multi-Document Search & Query System

An AI/ML document intelligence prototype that allows users to upload multiple organisational documents, search them using natural-language queries, retrieve relevant information, and identify the source document and page containing the supporting information.

## 🎯 Objective

The system was developed to make a collection of organisational documents searchable, understandable and useful for decision-making.

It supports:

- Multiple document input
- Document processing
- Natural-language search
- AI-based question answering
- Source identification
- Page-wise references
- Relevance scoring
- Document-wise search results

## 🏗️ System Architecture

```text
User
  │
  ▼
Streamlit Web Interface
  │
  ▼
Multiple Document Upload
  │
  ▼
Text Extraction
  │
  ├── PDF → PyMuPDF
  ├── DOCX → python-docx
  └── TXT → Text Reader
  │
  ▼
Text Cleaning
  │
  ▼
Document Chunking
  │
  ▼
TF-IDF Representation
  │
  ▼
Cosine Similarity Retrieval
  │
  ▼
Relevant Passages
  │
  ▼
Grounded Answer
  │
  ▼
Source Identification
(Document + Page + Relevance)

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| **Python** | Core application |
| **Streamlit** | Web interface |
| **PyMuPDF** | PDF text extraction |
| **python-docx** | DOCX processing |
| **Scikit-learn** | TF-IDF and cosine similarity |
| **NumPy** | Numerical processing |
| **OpenAI API** | Optional answer-generation layer |

---

## 🔄 How It Works

### 1. Document Upload

Users can upload multiple **PDF, TXT or DOCX** documents.

### 2. Text Extraction

The system extracts readable text while preserving **document and page information**.

### 3. Text Cleaning

Unnecessary whitespace and formatting artifacts are removed to make the extracted content suitable for processing.

### 4. Chunking

Documents are divided into smaller searchable passages.

This allows the system to retrieve specific relevant sections instead of processing an entire document for every query.

### 5. Vector Representation

**TF-IDF (Term Frequency-Inverse Document Frequency)** converts document passages into numerical representations.

### 6. Retrieval

The user's natural-language question is represented using the same TF-IDF model.

**Cosine similarity** is then used to compare the query with document passages and rank them according to their relevance.

### 7. Grounded Answer

The most relevant retrieved passages are presented as the evidence for the answer.

This helps keep the response tied to the information contained in the uploaded documents.

### 8. Source Identification

Each retrieved result retains:

- 📄 Document name
- 📑 Page number
- 📝 Relevant passage
- 📊 Relevance score

---

## 💻 Installation

### 1. Clone the Repository

```bash
git clone YOUR_REPOSITORY_URL
cd AI-Document-Intelligence
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment

**Windows:**

```bash
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the Application

```bash
python -m streamlit run app.py
```

The application will be available at:

```text
http://localhost:8501
```

---

## 🔎 Example Queries

The application supports natural-language questions such as:

```text
Which entities have pending server procurement and what amount was allocated?
```

```text
What is the procurement status of Project C?
```

```text
What is the current asset situation at Charlie Centre?
```

---

## ⭐ Key Features

### 📂 Multi-Document Search

The user can search across the complete uploaded document collection instead of manually searching individual files.

### 📚 Source Traceability

Results retain document and page metadata so that information can be verified against the original source.

### 📊 Document-Wise Retrieval

The application shows which documents contributed relevant passages to a query.

### 📈 Relevance Scoring

Retrieved passages are ranked using similarity scores, allowing the user to see which passages were considered more relevant to the query.

---

## 🔐 Security Considerations

For deployment with sensitive organisational documents, the system can be extended with:

- 🔑 Authentication
- 👥 Role-based access control
- 🔒 Encryption
- 🗄️ Secure document storage
- 📋 Audit logging
- 🖥️ Local/on-premise LLM deployment
- 📑 Document access permissions
- 🛡️ Prompt-injection protection

> **Note:** Assessment documents are intentionally excluded from this repository.

---

## 🚀 Future Improvements

The current retrieval architecture can be extended with:

- 🧠 Sentence Transformer embeddings
- ⚡ FAISS / vector database
- 🤖 Local LLM integration
- 🖨️ OCR for scanned documents
- 📚 Multi-document summarisation
- 🔄 Document comparison
- 💬 Conversational follow-up questions
- 🏷️ Document classification
- 🔦 Relevant passage highlighting
- 🎯 Confidence estimation
- ♻️ Duplicate document detection
- ➕ Incremental document indexing

---

## 📌 Project Scope

This implementation focuses on a **lightweight and explainable retrieval pipeline** suitable for a rapid prototype.

The current retrieval layer uses **TF-IDF and cosine similarity**. It can later be upgraded to embedding-based semantic retrieval without redesigning the document ingestion and source-traceability components.

The modular architecture also allows an approved or local LLM to be integrated as an answer-generation layer.

---

## 👨‍💻 Author

**Yashas Raina**

B.Tech — Artificial Intelligence & Machine Learning