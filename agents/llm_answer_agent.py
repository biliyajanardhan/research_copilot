from services.openai_client import client, CHAT_DEPLOYMENT

class LLMAnswerAgent:
    def answer(self, query: str):
        response = client.chat.completions.create(
            model=CHAT_DEPLOYMENT,   # ✅ Azure deployment name
            messages=[
                {"role": "system", "content": "You are an AI tutor."},
                {"role": "user", "content": query}
            ],
            temperature=0.3
        )

        return {
            "answer": response.choices[0].message.content,
            "sources": []
        }
