from pypdf import PdfReader

class PDFParserAgent:
    def extract_text(self, pdf_path):
        reader = PdfReader(pdf_path)
        pages = []

        for page in reader.pages:
            text = page.extract_text()
            if text:
                pages.append(text)

        return "\n".join(pages)
