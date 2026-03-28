# 🏥 Medi Chat — AI-Powered Medical Report Assistant      - Link : https://your-personal-medical-assistant.streamlit.app/

> Upload your medical PDF and have a real conversation about it — in plain English.

Medical Chat is a **RAG-based conversational AI personal assistant** built with LangGraph, LangChain, ChromaDB, and Claude (Anthropic). It reads your medical reports, explains every term, interprets your specific lab values, and gives you personalized suggestions — including diet, lifestyle, and follow-up questions to ask your doctor.

---

## ✨ What It Does

- 📄 **Upload any medical PDF** — lab reports, blood work, radiology summaries, discharge notes
- 🔬 **Explains medical terminology** in plain language tailored to your report
- 📊 **Interprets your specific values** — tells you what *your* hemoglobin, eGFR, or cholesterol actually means
- 🥗 **Diet & lifestyle suggestions** based on your results
- 💬 **Conversational Q&A** — ask follow-up questions naturally, just like talking to a doctor
- 🧠 Powered by **Claude (Anthropic)** + **LangGraph agentic pipeline** + **ChromaDB vector store**

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| LLM | Claude (Anthropic API) |
| Orchestration | LangGraph + LangChain |
| Vector Store | ChromaDB |
| PDF Parsing | pdfplumber |
| Embeddings | sentence-transformers |
| UI | Streamlit |

---

## 🚀 Setup & Run (Windows)

### Step 1 — Clone the repo

```bash
git clone https://github.com/priya-zha/medical-chat.git
cd medical-chat\medical-chat
```

Or navigate to where you downloaded it:

```
cd C:\Users\pj351\Desktop\medical-chat
```

### Step 2 — Create and activate a virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

### Step 3 — Install dependencies

```bash
pip install anthropic langchain langgraph langchain-anthropic langchain-community langchain-core pdfplumber chromadb streamlit sentence-transformers
```

### Step 4 — Set your Anthropic API key

```bash
set ANTHROPIC_API_KEY=your_key_here
```

### Step 5 — Run the app

```bash
streamlit run app.py
```

Your browser will open at `http://localhost:8501`

---

## 💬 How to Use

1. Upload your medical PDF from the **sidebar**
2. Wait a few seconds for it to be indexed
3. Ask anything in the chat

**Example questions:**
- What does my hemoglobin level mean?
- Is my blood pressure normal?
- Explain what eGFR means for my kidneys
- Should I be worried about my cholesterol?
- What foods should I eat based on my report?
- What follow-up tests should I ask my doctor about?

---

## 📁 Project Structure

```
medical-chat/
├── app.py             ← Streamlit UI & chat interface
├── graph.py           ← LangGraph agentic orchestration
├── nodes.py           ← Ingest, retrieve, and generate logic
├── vectorstore.py     ← ChromaDB vector store setup
├── requirements.txt   ← All dependencies
└── README.md
```

---

## ⚠️ Disclaimer

This tool is for **informational purposes only**. It does not constitute medical advice. Always consult a qualified healthcare professional for any medical decisions.

---

*Built by [Priya Jha](https://github.com/priya-zha)*
