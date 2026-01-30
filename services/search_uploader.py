import os
import uuid
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv

load_dotenv()

class SearchUploader:
    def __init__(self):
        self.client = SearchClient(
            endpoint=os.getenv("AZURE_SEARCH_ENDPOINT"),
            index_name=os.getenv("AZURE_SEARCH_INDEX"),
            credential=AzureKeyCredential(os.getenv("AZURE_SEARCH_KEY"))
        )

    def upload_chunks(self, chunks, embeddings, source):
        docs = []

        for text, vector in zip(chunks, embeddings):
            docs.append({
                "id": str(uuid.uuid4()),
                "content": text,
                "embedding": vector,
                "source": source
            })

        self.client.upload_documents(docs)
        print(f"✅ Uploaded {len(docs)} chunks")
