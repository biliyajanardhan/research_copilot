import json
from agents.planner_agent import PlannerAgent
from agents.llm_answer_agent import LLMAnswerAgent
from agents.research_agent import ResearchAgent
from agents.rag_qa_agent import RAGQAAgent


def is_paper_query(query: str) -> bool:
    """
    Domain-agnostic detection of paper intent.
    Works for ALL research fields.
    """
    q = query.lower()

    intent_phrases = [
        "research paper",
        "research papers",
        "academic paper",
        "academic papers",
        "survey paper",
        "survey papers",
        "review paper",
        "review papers",
        "find papers",
        "get papers",
        "show papers",
        "download paper",
        "download pdf",
        "arxiv",
        "ieee",
        "springer",
        "elsevier",
        "nature paper",
        "science paper",
        "journal paper",
        "conference paper",
    ]

    # Strong verbs indicating discovery
    discovery_verbs = [
        "find",
        "search",
        "list",
        "show",
        "give",
        "recommend",
        "fetch",
    ]

    # If user explicitly asks for papers
    if any(p in q for p in intent_phrases):
        return True

    # If user combines discovery verbs + topic
    if any(v in q for v in discovery_verbs) and "paper" in q:
        return True

    # Advanced queries like:
    # "Find advanced research on quantum entanglement"
    if any(v in q for v in discovery_verbs) and any(
        k in q for k in ["research", "study", "studies", "literature"]
    ):
        return True

    return False


class MasterAgent:
    def __init__(self):
        self.planner = PlannerAgent()
        self.llm = LLMAnswerAgent()
        self.research = ResearchAgent()
        self.rag = RAGQAAgent()

    def run(self, query: str):
        if is_paper_query(query):
            result = self.research.search_and_summarize(query)
            return {
                "answer": result["answer"],   # already string
                "sources": result.get("sources", [])
            }

        intent = self.planner.route(query)

        if intent == "general":
            result = self.llm.answer(query)

        elif intent == "research":
            result = self.research.run(query)

        elif intent == "rag":
            result = self.rag.answer(query)

        else:
            result = self.llm.answer(query)

        # 🔒 HARD GUARANTEE
        answer = result.get("answer", "")
        if not isinstance(answer, str):
            answer = json.dumps(answer, indent=2)

        return {
            "answer": answer,
            "sources": result.get("sources", [])
        }
