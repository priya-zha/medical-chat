#!/bin/bash

echo "🏥 Setting up Medical Report Chatbot..."

# Create virtual environment
python3 -m venv venv
echo "✅ Virtual environment created"

# Activate it
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip --quiet

# Install all dependencies
echo "📦 Installing packages (this may take 2-3 mins)..."
pip install anthropic langchain langgraph langchain-anthropic \
    langchain-community langchain-core pdfplumber chromadb \
    streamlit sentence-transformers --quiet

echo ""
echo "✅ All packages installed!"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  To run the app:"
echo ""
echo "  1. Set your API key:"
echo "     export ANTHROPIC_API_KEY=your_key_here"
echo ""
echo "  2. Activate the virtual env:"
echo "     source venv/bin/activate"
echo ""
echo "  3. Run:"
echo "     streamlit run app.py"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
