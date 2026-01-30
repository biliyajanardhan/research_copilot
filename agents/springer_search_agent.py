import requests
import os

class SpringerSearchAgent:
    BASE_URL = "https://api.springernature.com/openaccess/json"

    def __init__(self):
        self.api_key = os.getenv("SPRINGER_API_KEY")
        if not self.api_key:
            raise ValueError("SPRINGER_API_KEY not set in environment")

    def search(self, query: str, max_results: int = 10):
        params = {
            "q": query,
            "api_key": self.api_key,
            "p": max_results
        }

        response = requests.get(self.BASE_URL, params=params, timeout=20)
        response.raise_for_status()

        data = response.json()
        records = data.get("records", [])

        papers = []

        for r in records:
            title = r.get("title")
            abstract = r.get("abstract")
            doi = r.get("doi")

            # PDF link (only if Open Access)
            pdf_url = None
            for url in r.get("url", []):
                if url.get("format") == "pdf":
                    pdf_url = url.get("value")

            if not title or not abstract:
                continue

            papers.append({
                "title": title,
                "summary": abstract,
                "pdf_url": pdf_url,
                "doi": doi,
                "source": "springer"
            })

        return papers
