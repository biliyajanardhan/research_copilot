from services.openai_client import client, CHAT_DEPLOYMENT

resp = client.chat.completions.create(
    model=CHAT_DEPLOYMENT,
    messages=[{"role":"user","content":"What is machine learning"}]
)

print(resp.choices[0].message.content)
