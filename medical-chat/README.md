# 🏥 Medical Report Chatbot

A RAG-based conversational AI that reads your medical PDF and answers questions in plain English — explaining terms AND what your specific values mean for your body.

---

## 🚀 Setup (one time only)

### Step 1 — Extract the zip
Unzip `medical-chat.zip` anywhere on your machine.

```bash
cd medical-chat
```

### Step 2 — Run the setup script
```bash
bash setup.sh
```
This creates a virtual environment and installs all packages automatically.

### Step 3 — Set your Anthropic API key
```bash
export ANTHROPIC_API_KEY=your_key_here
```

### Step 4 — Activate the virtual env
```bash
source venv/bin/activate
```

### Step 5 — Run the app
```bash
streamlit run app.py
```

Your browser will open automatically at `http://localhost:8501`

---

## 💬 How to use

1. Upload your medical PDF from the **sidebar**
2. Wait ~5 seconds for it to index
3. Type any question in the chat box

**Example questions:**
- What does my hemoglobin level mean?
- Is my blood pressure normal?
- Explain what eGFR means for my kidneys
- Should I be worried about my cholesterol?

---

## 📁 Project Structure

```
medical-chat/
├── app.py            ← Streamlit UI
├── graph.py          ← LangGraph orchestration
├── nodes.py          ← Ingest, retrieve, generate logic
├── vectorstore.py    ← ChromaDB setup
├── requirements.txt  ← All dependencies
├── setup.sh          ← One-click setup script
└── README.md
```

---

## ⚠️ Disclaimer
This tool is for informational purposes only. Always consult a qualified doctor for medical decisions.
