import numpy as np
from rag.embeddings import EmbeddingService

class RelevanceAgent:
    def __init__(self):
        self.embedder = EmbeddingService()

    def score(self, query: str, papers: list):
        query_vec = self.embedder.embed_text(query)

        for paper in papers:
            paper_vec = self.embedder.embed_text(
                paper["title"] + " " + paper["summary"]
            )
            similarity = np.dot(query_vec, paper_vec)
            paper["relevance"] = round(float(similarity * 100), 2)

        return sorted(papers, key=lambda x: x["relevance"], reverse=True)
