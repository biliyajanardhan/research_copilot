from services.openai_client import client, CHAT_DEPLOYMENT

class CategoryAgent:
    def detect(self, query: str) -> dict:
        """
        Detect research domain + arXiv category
        """
        prompt = f"""
Classify the research domain of this query.

Query:
"{query}"

Return JSON ONLY in this format:
{{
  "domain": "physics | biology | chemistry | computer_science | medicine | economics | interdisciplinary",
  "arxiv_category": "quant-ph | hep-th | cs.AI | cs.LG | q-bio | cond-mat | stat | math | econ"
}}
"""

        response = client.chat.completions.create(
            model=CHAT_DEPLOYMENT,
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        return eval(response.choices[0].message.content)
