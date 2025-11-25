from google import genai  
from google.genai import types
from google.genai import Client
import os
from dotenv import load_dotenv  

load_dotenv()

def get_client():
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    return genai.Client(api_key=GEMINI_API_KEY)

client = get_client()


def generate_summary(text):
    response = client.models.generate_content(
        model="models/gemini-2.0-flash",
        contents=f"""
Summarize the following text into short bullet points,
easy to learn format:

{text}
"""
    )
    return response.text


def generate_quiz(text, quiz_type="Multiple Choice"):

    prompt = f"""
Create a {10} question quiz based only on this content:

{text}

Rules:
- Each question must have exactly 4 options: A, B, C, D
- Write the answer on a separate line formatted like: Answer: C
- No numbering inside options
- Keep formatting clean

Example Format:

Q1: What is AI?
A) A language
B) A subject
C) Artificial Intelligence
D) None
Answer: C

Make sure the output follows this format.
"""

    response = client.models.generate_content(
        model="models/gemini-2.0-flash",
        contents=prompt
    )
    
    return response.text
