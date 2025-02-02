import PdfUploader from "@/components/PdfUploader";

export default function Home() {
  return (
    <main className="min-h-screen flex flex-col items-center justify-center bg-background text-text px-4">
      <h1 className="text-4xl font-bold text-primary">PDF Companion AI</h1>
      <p className="text-lg mt-4 text-secondary">
        Upload a PDF and ask AI anything!
      </p>

      <div className="mt-6">
        <PdfUploader />
      </div>
    </main>
  );
}
