document.getElementById("pdf-upload")?.addEventListener("change", (event) => {
  const file = (event.target as HTMLInputElement).files?.[0];
  if (file) {
    uploadPDF(file);
  }
});

document.getElementById("send-button")?.addEventListener("click", () => {
  const input = document.getElementById("chat-input") as HTMLInputElement;
  const question = input.value;
  if (question) {
    sendQuestion(question);
    input.value = "";
  }
});

async function uploadPDF(file: File) {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch("/upload", {
    method: "POST",
    body: formData,
  });
    alert("PDF uploaded successfully!");
  } else {
    alert("Failed to upload PDF.");
  }
}

async function sendQuestion(question: string) {
  const response = await fetch("/ask", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ question }),
  });

  if (response.ok) {
    const data = await response.json();
    const chatOutput = document.getElementById("chat-output");
    if (chatOutput) {
      chatOutput.innerHTML += `<p><strong>You:</strong> ${question}</p>`;
      chatOutput.innerHTML += `<p><strong>AI:</strong> ${data.answer}</p>`;
    }
  } else {
    alert("Failed to get an answer.");
  }
}
