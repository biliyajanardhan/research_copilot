class PaperAggregator:
    def merge(self, *paper_lists):
        seen = set()
        merged = []

        for papers in paper_lists:
            for paper in papers:
                # Prefer DOI, fallback to title
                key = paper.get("doi") or paper.get("title")

                if not key:
                    continue

                key = key.lower().strip()

                if key in seen:
                    continue

                seen.add(key)
                merged.append(paper)

        return merged
