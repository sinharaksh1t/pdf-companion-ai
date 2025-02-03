import os
import shutil

from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from pydantic import BaseModel
from utils.pdf_processor import extract_text_from_pdf

# Load environment variables
load_dotenv()

# Set OpenAI API key
# openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
openai_client = OpenAI(
    base_url="https://api.groq.com/openai/v1", api_key=os.getenv("GROQ_API_KEY")
)


app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    # Allow only from localhost:3001 where the frontend is running
    allow_origins=["http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract text from PDF
    extracted_text = extract_text_from_pdf(file_path)

    return {
        "filename": file.filename,
        "message": "Upload successful",
        "text": extracted_text,
    }


# Create BaseModel for /ask API
class Input(BaseModel):
    question: str
    document_text: str


@app.post("/ask")
async def ask_question(input: Input):
    question, document_text = input.question, input.document_text
    """Process the user's question with OpenAI."""
    try:
        response = openai_client.chat.completions.create(
            # model="gpt-4o-mini",  # Or whichever model you prefer
            # model="llama-guard-3-8b",  # Or whichever model you prefer
            model="deepseek-r1-distill-llama-70b",  # Or whichever model you prefer
            messages=[
                {
                    "role": "user",
                    "content": f"Answer the following question based on the document text:\n\n{document_text}\n\nQuestion: {question}",
                }
            ],
        )
        answer = response.choices[0].message.content
        return {"answer": answer}
    except Exception as e:
        return {"error": str(e)}
