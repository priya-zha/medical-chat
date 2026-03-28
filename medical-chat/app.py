import streamlit as st
import tempfile
import os
from graph import run_ingest, run_chat_turn

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Medical Report Chat",
    page_icon="🏥",
    layout="centered"
)

st.title("🏥 Medical Report Interpreter")
st.caption("Upload your medical PDF and ask questions in plain English.")

# ── Session state init ────────────────────────────────────────────────────────
# Session state = memory that persists while the app is open
if "graph_state" not in st.session_state:
    st.session_state.graph_state = None  # holds the full LangGraph state

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []   # list of (role, message) for display

if "pdf_ready" not in st.session_state:
    st.session_state.pdf_ready = False


# ── Sidebar: PDF upload ───────────────────────────────────────────────────────
with st.sidebar:
    st.header("📄 Upload Report")
    uploaded_file = st.file_uploader("Choose a medical PDF", type=["pdf"])

    if uploaded_file and not st.session_state.pdf_ready:
        with st.spinner("Reading and indexing your report..."):
            # Save uploaded file to a temp path so pdfplumber can read it
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(uploaded_file.read())
                tmp_path = tmp.name

            # Run the ingest node
            state = run_ingest(tmp_path)
            os.unlink(tmp_path)  # clean up temp file

            st.session_state.graph_state = state
            st.session_state.pdf_ready = True

        st.success(f"✅ Report loaded! ({state['num_chunks']} sections indexed)")

    if st.session_state.pdf_ready:
        if st.button("🗑️ Clear & Upload New Report"):
            st.session_state.graph_state = None
            st.session_state.chat_history = []
            st.session_state.pdf_ready = False
            st.rerun()

    st.divider()
    st.markdown("**Tips — try asking:**")
    st.markdown("- What does my hemoglobin level mean?")
    st.markdown("- Is my blood pressure normal?")
    st.markdown("- Explain what eGFR means for my kidneys")
    st.markdown("- Should I be worried about my cholesterol?")


# ── Main chat area ────────────────────────────────────────────────────────────
if not st.session_state.pdf_ready:
    st.info("👈 Please upload your medical PDF from the sidebar to get started.")
else:
    # Display chat history
    for role, message in st.session_state.chat_history:
        with st.chat_message(role):
            st.markdown(message)

    # Chat input
    user_input = st.chat_input("Ask about your medical report...")

    if user_input:
        # Show user message immediately
        with st.chat_message("user"):
            st.markdown(user_input)
        st.session_state.chat_history.append(("user", user_input))

        # Run the graph
        with st.chat_message("assistant"):
            with st.spinner("Analyzing your report..."):
                updated_state = run_chat_turn(
                    st.session_state.graph_state,
                    user_input
                )
                answer = updated_state["last_answer"]

            st.markdown(answer)

        # Save updated state and answer
        st.session_state.graph_state = updated_state
        st.session_state.chat_history.append(("assistant", answer))
