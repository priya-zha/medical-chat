import pdfplumber
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage

from vectorstore import get_collection, store_chunks, retrieve_chunks

# ── System prompt ────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are a friendly and knowledgeable medical report interpreter.

You will receive:
1. Relevant excerpts from a patient's medical report
2. The patient's question

Your job is to ALWAYS respond in two clear parts:

**What it means (the term):**
Explain the medical term or test in plain, simple English — as if explaining to someone with no medical background.

**What it means for YOU (your report):**
Look at the actual value in the patient's report and explain what that specific number or result means for their body. Be honest but calm. If a value is outside normal range, say so clearly but without causing panic.

Always end with: "For any concerns, please consult your doctor."

Never make up values. Only use what's in the provided report excerpts."""


# ── LLM setup ────────────────────────────────────────────────────────────────
def get_llm():
    return ChatAnthropic(model="claude-sonnet-4-20250514", temperature=0.2)


# ── Node 1: Ingest PDF ───────────────────────────────────────────────────────
def ingest_node(state: dict) -> dict:
    """
    Reads the uploaded PDF, cuts it into chunks, stores in ChromaDB.
    This runs once when the user uploads a file.
    """
    pdf_path = state["pdf_path"]

    # Step 1: Extract raw text from PDF
    raw_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                raw_text += text + "\n"

    # Step 2: Cut into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,       # each chunk = ~500 characters
        chunk_overlap=50      # slight overlap so context isn't lost at edges
    )
    chunks = splitter.split_text(raw_text)

    # Step 3: Store in ChromaDB
    collection = get_collection()
    store_chunks(chunks, collection)

    return {
        **state,
        "pdf_loaded": True,
        "num_chunks": len(chunks),
        "collection": collection
    }


# ── Node 2: Retrieve relevant chunks ────────────────────────────────────────
def retrieve_node(state: dict) -> dict:
    """
    Takes the user's latest question and finds the most relevant
    chunks from the stored PDF.
    """
    question = state["messages"][-1]["content"]  # last user message
    collection = state["collection"]

    relevant_chunks = retrieve_chunks(question, collection, n_results=4)

    context = "\n\n---\n\n".join(relevant_chunks)

    return {
        **state,
        "context": context
    }


# ── Node 3: Generate answer ──────────────────────────────────────────────────
def generate_node(state: dict) -> dict:
    """
    Sends the question + retrieved context + chat history to Claude.
    Gets back a clear, personalized medical explanation.
    """
    llm = get_llm()
    context = state["context"]
    messages = state["messages"]

    # Build the user message with context injected
    latest_question = messages[-1]["content"]
    user_message_with_context = f"""Here are the relevant parts of my medical report:

{context}

My question: {latest_question}"""

    # Build message history for Claude (excluding the last message, we replaced it)
    history = []
    for msg in messages[:-1]:
        if msg["role"] == "user":
            history.append(HumanMessage(content=msg["content"]))
        else:
            history.append(HumanMessage(content=msg["content"]))  # simplified

    # Final call to Claude
    response = llm.invoke(
        [SystemMessage(content=SYSTEM_PROMPT)]
        + history
        + [HumanMessage(content=user_message_with_context)]
    )

    answer = response.content

    # Append assistant reply to message history
    updated_messages = messages + [{"role": "assistant", "content": answer}]

    return {
        **state,
        "messages": updated_messages,
        "last_answer": answer
    }
