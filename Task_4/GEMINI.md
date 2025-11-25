# Study notes — Project Spec

**Role**: Senior Python AI Engineer  
**Goal**: Build a **PDF Study Notes Summarizer & Quiz Generator** using OpenAgents SDK, Gemini API, Streamlit, PyPDF, and Context7 MCP Server.

## Overview
An AI agent that:
- Uploads PDFs  
- Extracts text  
- Generates summaries  
- Creates quizzes (MCQs + mixed formats)  
- Provides a simple Streamlit UI  
- Validates tool calls via Context7 MCP Server  

## Technical Guidelines
- **Minimalist**: Only documented SDK features, no extras  
- **API**: Connect to Gemini (`gemini-2.0-flash`) using `GEMINI_API_KEY`  
- **Error Handling**: Stop on errors, consult MCP docs, rewrite  
- **Dependencies**: Use `uv`, install only needed libraries  

## File Layout
```text
.
├── GEMINI.md
├── .env
├── app.py
├── modules/
│   ├── ai_engine.py
│   ├── pdf_handler.py
│   ├── ui_components.py
│   └── utils.py
├── requirements.txt
├── README.md
└── run.sh
