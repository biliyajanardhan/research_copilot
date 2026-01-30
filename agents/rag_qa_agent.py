from services.openai_client import client, CHAT_DEPLOYMENT
from services.retriever import VectorRetriever
from rag.embeddings import EmbeddingService
from agents.paper_memory import PaperMemory


class RAGQAAgent:
    def __init__(self):
        self.retriever = VectorRetriever()
        self.embedder = EmbeddingService()
        self.paper_memory = PaperMemory()

    def answer(self, query: str):
        # 1️⃣ Embed query
        query_vector = self.embedder.embed_text(query)

        # 2️⃣ Retrieve relevant chunks
        docs = self.retriever.search(query_vector, k=5)

        if not docs:
            return {
                "answer": "⚠️ I could not find relevant context in the knowledge base.",
                "citations": []
            }

        # 3️⃣ Build context with inline citations
        context = ""
        citations = []

        for i, d in enumerate(docs, 1):
            context += f"[{i}] {d['content']}\n\n"
            if d.get("metadata") and d["metadata"].get("pdf"):
                citations.append(d["metadata"]["pdf"])

        # 4️⃣ Prompt with strict grounding
        prompt = f"""
You are a research assistant.

Answer the question using ONLY the context below.
Cite sources inline using [1], [2], etc.
If the context is insufficient, say so clearly.

Context:
{context}

Question:
{query}
"""

        response = client.chat.completions.create(
            model=CHAT_DEPLOYMENT,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )

        answer_text = response.choices[0].message.content.strip()

        # 5️⃣ Append saved paper references (⭐ memory)
        saved_papers = self.paper_memory.list()

        if saved_papers:
            answer_text += "\n\n### 📚 Saved Paper References\n"
            for p in saved_papers:
                answer_text += f"- {p}\n"

        return {
            "answer": answer_text,
            "citations": citations
        }
