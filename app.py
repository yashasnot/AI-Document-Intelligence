import io
import re
import numpy as np
import streamlit as st
import fitz

from docx import Document
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ============================================================
# CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Document Intelligence",
    page_icon="🛡️",
    layout="wide"
)


# ============================================================
# HEADER
# ============================================================

st.title("🛡️ AI-Enabled Multi-Document Search & Query System")

st.caption(
    "Multi-document NLP search • Grounded question answering • "
    "Page-wise source identification"
)

st.divider()


# ============================================================
# TEXT CLEANING
# ============================================================

def clean_text(text):

    text = text.replace("\n", " ")

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ============================================================
# PDF PROCESSING
# ============================================================

def process_pdf(file):

    pages = []

    pdf = fitz.open(
        stream=file.getvalue(),
        filetype="pdf"
    )

    for page_number, page in enumerate(
        pdf,
        start=1
    ):

        text = page.get_text("text")

        text = clean_text(text)

        if text:

            pages.append({
                "text": text,
                "document": file.name,
                "page": page_number
            })

    pdf.close()

    return pages


# ============================================================
# DOCX PROCESSING
# ============================================================

def process_docx(file):

    document = Document(
        io.BytesIO(
            file.getvalue()
        )
    )

    text = "\n".join(
        paragraph.text
        for paragraph in document.paragraphs
    )

    text = clean_text(text)

    if text:

        return [{
            "text": text,
            "document": file.name,
            "page": 1
        }]

    return []


# ============================================================
# TXT PROCESSING
# ============================================================

def process_txt(file):

    text = file.getvalue().decode(
        "utf-8",
        errors="ignore"
    )

    text = clean_text(text)

    if text:

        return [{
            "text": text,
            "document": file.name,
            "page": 1
        }]

    return []


# ============================================================
# UNIVERSAL PROCESSOR
# ============================================================

def process_document(file):

    name = file.name.lower()

    if name.endswith(".pdf"):

        return process_pdf(file)

    elif name.endswith(".docx"):

        return process_docx(file)

    elif name.endswith(".txt"):

        return process_txt(file)

    return []


# ============================================================
# CHUNKING
# ============================================================

def create_chunks(pages):

    chunks = []

    for page in pages:

        text = page["text"]

        words = text.split()

        chunk_size = 120

        if len(words) <= chunk_size:

            chunks.append(page)

        else:

            for i in range(
                0,
                len(words),
                chunk_size
            ):

                chunk = " ".join(
                    words[
                        i:i + chunk_size
                    ]
                )

                if len(chunk) > 30:

                    chunks.append({

                        "text": chunk,

                        "document":
                            page["document"],

                        "page":
                            page["page"]

                    })

    return chunks


# ============================================================
# BUILD NLP INDEX
# ============================================================

def build_index(chunks):

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2)
    )

    matrix = vectorizer.fit_transform(
        texts
    )

    return vectorizer, matrix


# ============================================================
# SEARCH
# ============================================================

def search_documents(
    question,
    vectorizer,
    matrix,
    chunks,
    top_k=5
):

    question_vector = vectorizer.transform(
        [question]
    )

    scores = cosine_similarity(
        question_vector,
        matrix
    )[0]

    indices = np.argsort(
        scores
    )[::-1]

    results = []

    for index in indices[:top_k]:

        if scores[index] <= 0:
            continue

        result = chunks[index].copy()

        result["score"] = float(
            scores[index]
        )

        results.append(
            result
        )

    return results


# ============================================================
# EXTRACTIVE GROUNDED ANSWER
# ============================================================

def generate_answer(
    question,
    results
):

    question_words = set(
        re.findall(
            r"[a-zA-Z0-9₹]+",
            question.lower()
        )
    )

    candidates = []

    for result in results:

        sentences = re.split(
            r"(?<=[.!?])\s+",
            result["text"]
        )

        for sentence in sentences:

            sentence = sentence.strip()

            if not sentence:
                continue

            sentence_words = set(
                re.findall(
                    r"[a-zA-Z0-9₹]+",
                    sentence.lower()
                )
            )

            overlap = len(
                question_words &
                sentence_words
            )

            score = (
                overlap * 2
                + result["score"]
            )

            candidates.append(
                (
                    score,
                    sentence,
                    result
                )
            )

    candidates.sort(
        key=lambda x: x[0],
        reverse=True
    )

    selected = []

    seen = set()

    for score, sentence, result in candidates:

        key = sentence.lower()

        if key in seen:
            continue

        seen.add(key)

        selected.append(
            (sentence, result)
        )

        if len(selected) >= 4:
            break

    return selected


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("📂 Document Management")

    uploaded_files = st.file_uploader(
        "Upload multiple documents",
        type=[
            "pdf",
            "txt",
            "docx"
        ],
        accept_multiple_files=True
    )

    if uploaded_files:

        st.success(
            f"{len(uploaded_files)} documents selected"
        )

        for file in uploaded_files:

            st.write(
                "📄 " + file.name
            )

    st.divider()

    process_button = st.button(
        "⚙️ Process Documents",
        type="primary",
        use_container_width=True
    )


# ============================================================
# PROCESS DOCUMENTS
# ============================================================

if process_button:

    if not uploaded_files:

        st.error(
            "Please upload documents first."
        )

    else:

        with st.spinner(
            "Extracting and indexing documents..."
        ):

            pages = []

            for file in uploaded_files:

                pages.extend(
                    process_document(file)
                )

            chunks = create_chunks(
                pages
            )

            vectorizer, matrix = build_index(
                chunks
            )

            st.session_state.pages = pages

            st.session_state.chunks = chunks

            st.session_state.vectorizer = vectorizer

            st.session_state.matrix = matrix

            st.session_state.documents = [
                f.name
                for f in uploaded_files
            ]

            st.session_state.processed = True

        st.success(
            "✅ Documents processed successfully!"
        )


# ============================================================
# STATISTICS
# ============================================================

if st.session_state.get(
    "processed",
    False
):

    documents = st.session_state[
        "documents"
    ]

    pages = st.session_state[
        "pages"
    ]

    chunks = st.session_state[
        "chunks"
    ]

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "📄 Documents",
        len(documents)
    )

    col2.metric(
        "📑 Pages",
        len(pages)
    )

    col3.metric(
        "🧩 Chunks",
        len(chunks)
    )


# ============================================================
# QUERY
# ============================================================

st.subheader(
    "🔍 Ask a Natural-Language Question"
)

question = st.text_area(
    "Search across the entire document collection:",
    placeholder=
    "Which entities have pending server procurement and what amount was allocated?",
    height=100
)

search_button = st.button(
    "🔎 Search & Answer",
    use_container_width=True
)


# ============================================================
# SEARCH
# ============================================================

if search_button:

    if not st.session_state.get(
        "processed",
        False
    ):

        st.error(
            "Please process documents first."
        )

    elif not question.strip():

        st.warning(
            "Please enter a question."
        )

    else:

        results = search_documents(

            question,

            st.session_state[
                "vectorizer"
            ],

            st.session_state[
                "matrix"
            ],

            st.session_state[
                "chunks"
            ],

            top_k=5
        )

        st.session_state.results = results


# ============================================================
# RESULTS
# ============================================================

if "results" in st.session_state:

    results = st.session_state.results

    st.subheader(
        "🤖 Grounded Answer"
    )

    answer = generate_answer(
        question,
        results
    )

    if answer:

        for sentence, source in answer:

            st.write(
                "• " + sentence
            )

    else:

        st.warning(
            "No relevant information was found."
        )


    # ========================================================
    # SOURCES
    # ========================================================

    st.divider()

    st.subheader(
        "📚 Source Identification"
    )

    seen = set()

    for result in results:

        source = (
            result["document"],
            result["page"]
        )

        if source in seen:

            continue

        seen.add(source)

        relevance = (
            result["score"] * 100
        )

        with st.expander(

            f"📄 {result['document']} "
            f"| Page {result['page']} "
            f"| Relevance {relevance:.1f}%"

        ):

            st.write(
                result["text"]
            )

            st.caption(
                f"Source: {result['document']} "
                f"— Page {result['page']}"
            )


    # ========================================================
    # DOCUMENT-WISE RESULTS
    # ========================================================

    st.divider()

    st.subheader(
        "📊 Document-wise Search Results"
    )

    counts = {}

    for result in results:

        doc = result["document"]

        counts[doc] = (
            counts.get(doc, 0) + 1
        )

    for doc, count in counts.items():

        st.write(
            f"📄 **{doc}** — "
            f"{count} relevant passage(s)"
        )


    # ========================================================
    # ARCHITECTURE
    # ========================================================

    st.divider()

    st.caption(
        "Pipeline: Upload → Text Extraction → "
        "Cleaning → Chunking → TF-IDF NLP Representation → "
        "Cosine Similarity Retrieval → Grounded Answer → "
        "Document/Page Sources"
    )