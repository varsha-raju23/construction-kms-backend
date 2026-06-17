import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.0-flash")


def ask_gemini(question, documents):
    if not GEMINI_API_KEY:
        return "Gemini API key is missing. Please set GEMINI_API_KEY in your .env file."

    context = ""

    for doc in documents[:5]:
        title = doc.get("title", "Untitled Document")
        text = doc.get("extracted_text", "")

        context += f"\nDocument Title: {title}\n"
        context += f"Document Content:\n{text[:2000]}\n"

    prompt = f"""
You are a construction knowledge assistant for tunnel construction projects.

Answer the user's question using ONLY the given document content.

If the answer is not available in the documents, say:
"The answer is not available in the uploaded documents."

Documents:
{context}

User Question:
{question}

Answer:
"""

    response = model.generate_content(prompt)

    return response.text