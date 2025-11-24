import os
import asyncio
from pathlib import Path
import streamlit as st
from PyPDF2 import PdfReader
from openai_agents.core import Agent, Runner
from openai_agents import AsyncOpenAI, OpenAIChatCompletionsModel
from openai_agent.run import RunConfig
from dotenv import load_dotenv

# --- Load environment ---
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    st.error("GEMINI_API_KEY environment variable not set!")
    st.stop()

# --- Streamlit setup ---
st.set_page_config(page_title="PDF Study Notes Agent", layout="wide")
st.title("📚 PDF Summarizer & Quiz Generator (Gemini AI)")

uploaded_file = st.file_uploader("Upload your PDF", type="pdf")

# --- Function to extract text from PDF ---
def extract_pdf_text(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

# --- Async function to run agent ---
async def run_agent(pdf_text, num_questions=5):
    MODEL_NAME = "gemini-2.0-flash"

    # Gemini client
    external_client = AsyncOpenAI(
        api_key=GEMINI_API_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        timeout=60
    )

    model = OpenAIChatCompletionsModel(
        model=MODEL_NAME,
        openai_client=external_client
    )

    instructions = f"""
You are an expert AI assistant. 
1. Summarize the following PDF text concisely and clearly:
{pdf_text[:1000]}...
2. Then generate a quiz with max {num_questions} multiple-choice questions based on the original PDF content. 
Include answers for each question.
"""

    study_agent = Agent(
        name="StudyNotesAgent",
        instructions=instructions,
        model=model
    )

    config = RunConfig(model=model, model_provider=external_client, tracing_disabled=True)

    result = await Runner.run(study_agent, pdf_text, run_config=config)
    return result.final_output if result and result.final_output else "No output from agent."

# --- Main Streamlit workflow ---
if uploaded_file:
    # Save PDF to project folder temp dir
    temp_dir = Path(os.getcwd()) / ".gemini_tmp"
    temp_dir.mkdir(parents=True, exist_ok=True)
    file_path = temp_dir / uploaded_file.name
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"File saved: {file_path.name}")

    # Extract PDF text
    pdf_text = extract_pdf_text(file_path)
    if not pdf_text:
        st.error("Could not extract text from PDF. Is it image-based?")
        st.stop()

    # Show partial PDF text
    with st.expander("Preview PDF Text"):
        st.text_area("PDF content", pdf_text[:1000] + ("..." if len(pdf_text) > 1000 else ""), height=300)

    # Number of quiz questions (max 5)
    num_questions = st.slider("Number of Quiz Questions", 1, 5, 5)

    if st.button("Generate Summary & Quiz"):
        with st.spinner("Generating summary and quiz..."):
            output = asyncio.run(run_agent(pdf_text, num_questions))
            st.markdown(
                f"<div style='border:1px solid #ddd;padding:10px;border-radius:8px'>{output}</div>",
                unsafe_allow_html=True
            )
