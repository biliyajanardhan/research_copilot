from services.openai_client import client, EMBED_DEPLOYMENT

class EmbeddingService:
    def __init__(self):
        self.deployment = EMBED_DEPLOYMENT

    def embed_text(self, text: str) -> list[float]:
        response = client.embeddings.create(
            model=self.deployment,
            input=text
        )
        return response.data[0].embedding
