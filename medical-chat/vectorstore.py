import chromadb
from chromadb.utils import embedding_functions

# We use a free local embedding model — no extra API cost
EMBED_MODEL = "all-MiniLM-L6-v2"
COLLECTION_NAME = "medical_report"


def get_collection():
    """
    Creates (or connects to) a local ChromaDB collection.
    This is your 'filing cabinet' that stores all the PDF chunks.
    """
    client = chromadb.Client()  # runs in memory (no disk needed)

    ef = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=EMBED_MODEL
    )

    # get_or_create means: if it already exists, just open it
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=ef
    )

    return collection


def store_chunks(chunks: list[str], collection) -> None:
    """
    Takes a list of text chunks from the PDF and stores them in ChromaDB.
    Each chunk gets a unique ID so ChromaDB can track it.
    """
    # Clear old data first so a new PDF doesn't mix with a previous one
    existing = collection.count()
    if existing > 0:
        collection.delete(where={"source": "medical_pdf"})

    ids = [f"chunk_{i}" for i in range(len(chunks))]
    metadatas = [{"source": "medical_pdf"} for _ in chunks]

    collection.add(
        documents=chunks,
        ids=ids,
        metadatas=metadatas
    )


def retrieve_chunks(query: str, collection, n_results: int = 4) -> list[str]:
    """
    Given a user's question, finds the most relevant chunks from the PDF.
    This is the 'search the filing cabinet' step.
    """
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )

    # results["documents"] is a list of lists, we flatten it
    return results["documents"][0] if results["documents"] else []
