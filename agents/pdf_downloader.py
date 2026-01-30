import os
import re
import unicodedata
import requests


class PDFDownloaderAgent:
    def safe_filename(self, title: str, max_len=120):
        # Normalize unicode (μ → mu, etc.)
        title = unicodedata.normalize("NFKD", title)
        title = title.encode("ascii", "ignore").decode()

        # Remove LaTeX math blocks like $...$
        title = re.sub(r"\$.*?\$", "", title)

        # Replace arrows and slashes
        title = title.replace("->", "to").replace("/", "_")

        # Keep only filesystem-safe characters
        title = re.sub(r"[^a-zA-Z0-9._-]", "_", title)
        title = re.sub(r"_+", "_", title)

        return title.strip("_")[:max_len] + ".pdf"

    def download(self, url, title):
        # Ensure directory exists
        base_dir = "data/papers"
        os.makedirs(base_dir, exist_ok=True)

        # Sanitize filename
        filename = self.safe_filename(title)
        path = os.path.join(base_dir, filename)

        # Download PDF
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        with open(path, "wb") as f:
            f.write(response.content)

        return path
