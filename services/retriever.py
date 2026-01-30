import os
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv

load_dotenv()

class VectorRetriever:
    def __init__(self):
        self.client = SearchClient(
            endpoint=os.getenv("AZURE_SEARCH_ENDPOINT"),
            index_name=os.getenv("AZURE_SEARCH_INDEX"),
            credential=AzureKeyCredential(os.getenv("AZURE_SEARCH_KEY"))
        )

    def search(self, query_vector, k=5):
        vector_query = VectorizedQuery(
            vector=query_vector,
            k_nearest_neighbors=k,
            fields="embedding"
        )

        results = self.client.search(
            search_text=None,
            vector_queries=[vector_query],
            select=["content", "source"]
        )

        return [
            {
                "content": r["content"],
                "source": r["source"]
            }
            for r in results
        ]
