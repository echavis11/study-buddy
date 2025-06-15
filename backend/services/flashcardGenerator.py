import PyPDF2
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    return "\n".join(page.extract_text() for page in reader.pages if page.extract_text())

def generate_flashcards(text):
    prompt = (
        "You are an ai tutor. You will generate flashcards from the text provided. "
        "Each flashcard should be a JSON object with 'question' and 'answer' keys. "
        "The flashcards should focus on key facts, definitions, concepts and important information from the text. "
        f"Text:\n{text[:3000]}\n\n"
        '[{"question": "...", "answer": "..."}, ...]'
    )   
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    content = response.choices[0].message.content

    # Parse JSON from response
    import json
    try:
        content = response.choices[0].message.content
        flashcards = json.loads(content)
        return flashcards
    except Exception as e:
        print("Failed to parse OpenAI response:", e)
        return []

            