def build_prompt(question, docs):
    context = "\n\n".join(
        [f"[Source: {d['source']}]\n{d['content']}" for d in docs]
    )

    return f"""
You are a research assistant. Answer ONLY using the context below.
If the answer is not present, say "I don't know".

Context:
{context}

Question:
{question}

Answer:
""".strip()
