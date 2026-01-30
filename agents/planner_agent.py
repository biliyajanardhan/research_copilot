class PlannerAgent:
    def route(self, query: str) -> str:
        q = query.lower()

        if q.startswith(("what is", "explain", "define", "overview")):
            return "general"

        if any(k in q for k in ["research paper", "papers", "arxiv", "survey"]):
            return "research"

        if any(k in q for k in ["my document", "uploaded", "pdf", "rag"]):
            return "rag"

        # DEFAULT → LLM
        return "general"
