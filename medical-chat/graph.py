from langgraph.graph import StateGraph, END
from nodes import ingest_node, retrieve_node, generate_node
from typing import TypedDict, Any


# ── State schema ─────────────────────────────────────────────────────────────
# This is the "notepad" LangGraph carries through every node
class GraphState(TypedDict):
    pdf_path: str               # path to uploaded PDF
    pdf_loaded: bool            # has the PDF been ingested?
    num_chunks: int             # how many chunks were created
    collection: Any             # ChromaDB collection object
    messages: list[dict]        # full conversation history
    context: str                # retrieved chunks for current question
    last_answer: str            # Claude's latest response


# ── Build the chat graph ──────────────────────────────────────────────────────
def build_chat_graph():
    """
    Builds the LangGraph for answering questions about a medical PDF.

    Flow:
        retrieve → generate → END
        (ingest is called separately on PDF upload)
    """
    graph = StateGraph(GraphState)

    # Add nodes
    graph.add_node("retrieve", retrieve_node)
    graph.add_node("generate", generate_node)

    # Define flow: retrieve first, then generate, then done
    graph.set_entry_point("retrieve")
    graph.add_edge("retrieve", "generate")
    graph.add_edge("generate", END)

    return graph.compile()


# ── Ingest is a one-time setup, not part of the chat loop ────────────────────
def run_ingest(pdf_path: str) -> dict:
    """
    Runs the ingest node once when a PDF is uploaded.
    Returns the updated state with collection + chunk count.
    """
    initial_state = {
        "pdf_path": pdf_path,
        "pdf_loaded": False,
        "num_chunks": 0,
        "collection": None,
        "messages": [],
        "context": "",
        "last_answer": ""
    }
    return ingest_node(initial_state)


# ── Run one turn of the chat ──────────────────────────────────────────────────
def run_chat_turn(state: dict, user_question: str) -> dict:
    """
    Takes the current state + new user question,
    runs retrieve → generate, returns updated state.
    """
    # Append the new user question to message history
    updated_messages = state["messages"] + [
        {"role": "user", "content": user_question}
    ]

    updated_state = {**state, "messages": updated_messages}

    # Run through the graph
    app = build_chat_graph()
    result = app.invoke(updated_state)

    return result
