import arxiv

class PaperFetcherAgent:
    def fetch(self, query, max_results=5):
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.Relevance
        )

        papers = []
        for paper in search.results():
            papers.append({
                "title": paper.title,
                "authors": [a.name for a in paper.authors],
                "summary": paper.summary,
                "pdf_url": paper.pdf_url,
                "published": str(paper.published)
            })

        return papers
