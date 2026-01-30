from agents.category_agent import CategoryAgent
from agents.paper_memory import PaperMemory
from agents.relevance_agent import RelevanceAgent
from agents.web_search_agent import WebSearchAgent
from agents.springer_search_agent import SpringerSearchAgent
from agents.paper_aggregator import PaperAggregator

class ResearchAgent:
    def __init__(self):
        self.category = CategoryAgent()
        self.arxiv = WebSearchAgent()
        self.springer = SpringerSearchAgent()
        self.aggregator = PaperAggregator()
        self.relevance = RelevanceAgent()
        self.memory = PaperMemory()

    def search_and_summarize(self, query: str):
        category = self.category.detect(query)

        arxiv_papers = self.arxiv.search_arxiv(
            query=query,
            category=category.get("arxiv_category")
        )

        springer_papers = self.springer.search(query)

        merged = self.aggregator.merge(arxiv_papers, springer_papers)
        ranked = self.relevance.score(query, merged)

        if not ranked:
            return {
                "answer": "❌ No research papers found for this topic.",
                "sources": []
            }

        # ✅ BUILD MARKDOWN STRING (frontend-safe)
        md = "## 📚 Top Research Papers\n\n"

        for i, p in enumerate(ranked[:5], 1):
            md += f"""
### {i}. {p.get("title", "Untitled")}

{p.get("summary", "No abstract available.")}

🔗 **PDF:** {p.get("pdf_url", "N/A")}

---
"""

        return {
            "answer": md.strip(),   # ✅ STRING
            "sources": ranked[:5]
        }

    def run(self, query: str):
        # Fallback research reasoning (non-paper question)
        return {
            "answer": "🧠 Please ask a specific research question or request papers.",
            "sources": []
        }
