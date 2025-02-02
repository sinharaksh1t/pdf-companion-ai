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
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


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
async def ask_question(question: str, document_text: str):
    """Process the user's question with OpenAI."""
    print(question)
    print(document_text[:20])
    try:
        # response = openai_client.chat.completions.create(
        #     model="gpt-4o-mini",  # Or whichever model you prefer
        #     messages=[
        #         {
        #             "role": "user",
        #             "content": "Say this is a test",
        #         }
        #     ],
        #     response_format={"type": "json_object"},
        # )
        # # prompt=f"Answer the following question based on the document text:\n\n{document_text}\n\nQuestion: {question}",
        # # max_tokens=150,
        # answer = response.choices[0].text.strip()
        return {"answer": "hello this is the answer"}
    except Exception as e:
        return {"error": str(e)}
