from agents.pdf_downloader import PDFDownloaderAgent
from agents.pdf_parser import PDFParserAgent
from rag.chunking import chunk_text
from rag.embeddings import EmbeddingService
from services.search_uploader import SearchUploader

class IngestionAgent:
    def __init__(self):
        self.downloader = PDFDownloaderAgent()
        self.parser = PDFParserAgent()
        self.embedder = EmbeddingService()
        self.uploader = SearchUploader()

    def ingest(self, paper):
        pdf_path = self.downloader.download(
            paper["pdf_url"],
            paper["title"].replace(" ", "_")[:50]
        )

        text = self.parser.extract_text(pdf_path)
        chunks = chunk_text(text)

        embeddings = [self.embedder.embed_text(c) for c in chunks[:10]]

        self.uploader.upload_chunks(
            chunks[:10],
            embeddings,
            source=paper["title"]
        )
    
    class IngestionAgent:
        def ingest_paper(self, paper):
            content = f"""
    Title: {paper['title']}
    Source: {paper['source']}
    Summary: {paper['summary']}
    PDF: {paper['pdf_url']}
    """

            self.vector_store.add_document(
                content=content,
                metadata={
                    "title": paper["title"],
                    "pdf": paper["pdf_url"],
                    "source": paper["source"]
                }
            )
