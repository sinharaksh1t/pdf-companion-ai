import os
import shutil

from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
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
        # Return only the first 500 characters for preview
        "text": extracted_text[:500],
    }


@app.post("/ask")
async def ask_question(
    question: str = "What is this doc about?", document_text: str = "My name is Jeff"
):
    """Process the user's question with OpenAI."""
    try:
        # response = openai_client.chat.completions.create(
        #     # model="gpt-4o-mini",  # Or whichever model you prefer
        #     model="llama-guard-3-8b",  # Or whichever model you prefer
        #     messages=[
        #         {
        #             "role": "user",
        #             "content": f"Answer the following question based on the document text:\n\n{document_text}\n\nQuestion: {question}",
        #         }
        #     ],
        #     # response_format={"type": "json_object"},
        # )
        # # # max_tokens=150,
        # answer = response.choices[0].message.content
        return {"answer": f"Hi my name is: {question}, {document_text[:20]}"}
    except Exception as e:
        return {"error": str(e)}
