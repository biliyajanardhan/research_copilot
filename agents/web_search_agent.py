import feedparser
from urllib.parse import quote_plus


class WebSearchAgent:
    def search_arxiv(self, query, category=None, max_results=10):
        # 1️⃣ Build arXiv search query (DO NOT encode yet)
        if category:
            arxiv_query = f"cat:{category} AND all:{query}"
        else:
            arxiv_query = f"all:{query}"

        # 2️⃣ Encode once
        encoded_query = quote_plus(arxiv_query)

        # 3️⃣ arXiv API URL
        url = (
            "http://export.arxiv.org/api/query?"
            f"search_query={encoded_query}"
            f"&start=0"
            f"&max_results={max_results}"
            f"&sortBy=relevance"
        )

        feed = feedparser.parse(url)

        papers = []

        for entry in feed.entries:
            pdf_url = None

            for link in entry.links:
                if link.get("type") == "application/pdf":
                    pdf_url = link.href
                    break

            if not pdf_url:
                continue

            papers.append({
                "title": entry.title.strip(),
                "summary": entry.summary.strip(),
                "pdf_url": pdf_url,
                "arxiv_id": entry.get("id"),
                "published": entry.get("published"),
                "categories": [t.term for t in entry.get("tags", [])],
                "source": "arxiv"
            })

        return papers
