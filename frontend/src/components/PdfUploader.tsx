"use client";

import { useState } from "react";
import { useDropzone } from "react-dropzone";
import classNames from "classNames";

export default function PdfUploader() {
  const [file, setFile] = useState<File | null>(null);
  const [uploadStatus, setUploadStatus] = useState<string | null>(null);
  const [extractedText, setExtractedText] = useState<string | null>(null);
  const [question, setQuestion] = useState<string>("");
  const [answer, setAnswer] = useState<string | null>(null);

  const { getRootProps, getInputProps } = useDropzone({
    accept: { "application/pdf": [".pdf"] },
    multiple: false,
    onDrop: (acceptedFiles) => {
      setFile(acceptedFiles[0]);
      setExtractedText(null); // Reset extracted text on new upload
      setAnswer(null);
    },
  });

  const handleUpload = async () => {
    if (!file) {
      console.log("No file found, returning");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://localhost:8000/upload", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      setUploadStatus(data.message);
      setExtractedText(data.text);
    } catch (error) {
      setUploadStatus("Upload failed");
      setExtractedText(null);
    }
  };

  const handleAsk = async () => {
    if (!question || !extractedText) return;
    console.log(question, extractedText);

    try {
      const response = await fetch("http://localhost:8000/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          question: question,
          document_text: extractedText,
        }),
      });

      const data = await response.json();
      if (data.answer) {
        setAnswer(data.answer);
      } else {
        setAnswer("Sorry, I couldn't find an answer.");
      }
    } catch (error) {
      setAnswer("Error while asking the question.");
    }
  };

  return (
    <div className="flex flex-col items-center p-6 border-2 border-dashed border-gray-400 rounded-lg bg-white shadow-md w-full max-w-lg">
      <div {...getRootProps()} className="w-full text-center cursor-pointer">
        <input {...getInputProps()} />
        <p className="text-gray-600">
          {file
            ? `Selected: ${file.name}`
            : "Drag & drop a PDF here or click to select one"}
        </p>
      </div>

      {file && (
        <div className="mt-4">
          <button
            className="px-4 py-2 bg-primary text-white rounded-md shadow-md hover:bg-indigo-700 transition"
            onClick={handleUpload}
          >
            Upload PDF
          </button>
          {uploadStatus && (
            <p
              className={classNames("mt-2", {
                "text-red-600": uploadStatus.includes("failed"),
                "text-green-600": uploadStatus.includes("successful"),
              })}
            >
              {uploadStatus}
            </p>
          )}
          {extractedText && (
            <div className="mt-4 p-3 bg-gray-100 border border-gray-300 rounded-md max-h-40 overflow-y-auto text-sm text-gray-800">
              <strong>Extracted Text Preview:</strong>
              <p>{extractedText}</p>
            </div>
          )}
        </div>
      )}

      {extractedText && (
        <div className="mt-6 w-full">
          <textarea
            className="w-full p-3 border border-gray-300 rounded-md"
            placeholder="Ask a question about the document"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
          />
          <button
            onClick={handleAsk}
            className="mt-2 px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-700"
          >
            Ask Question
          </button>
          {answer && (
            <div className="mt-4 p-3 bg-gray-100 border border-gray-300 rounded-md text-sm text-gray-800">
              <strong>Answer:</strong>
              <p>{answer}</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
