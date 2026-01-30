import os
import json
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
import anyio

from agents.master_agent import MasterAgent

# -----------------------------------------------------------------------------
# App setup
# -----------------------------------------------------------------------------

app = FastAPI()

app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SESSION_SECRET", "dev-secret-key"),
)

templates = Jinja2Templates(directory="ui/templates")
agent = MasterAgent()

# -----------------------------------------------------------------------------
# Routes
# -----------------------------------------------------------------------------

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


@app.post("/ask-stream")
async def ask_stream(query: str = Form(...)):

    async def event_generator():
        try:
            # 1️⃣ Initial status event (no content yet)
            yield f"data: {json.dumps({'status': 'searching'})}\n\n"

            # 2️⃣ Run agent in thread (non-blocking)
            result = await anyio.to_thread.run_sync(agent.run, query)

            answer = result.get("answer", "")

            # 3️⃣ Ensure answer is always a string
            if not isinstance(answer, str):
                answer = json.dumps(answer, indent=2)

            # 4️⃣ Send final content
            yield f"data: {json.dumps({'token': answer})}\n\n"

            # 5️⃣ Signal completion
            yield f"data: {json.dumps({'done': True})}\n\n"

        except Exception as e:
            # 6️⃣ Error handling (still close stream properly)
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
            yield f"data: {json.dumps({'done': True})}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )


@app.post("/save-paper")
async def save_paper(url: str = Form(...)):
    """
    Save a research paper URL for later processing.
    """
    await anyio.to_thread.run_sync(agent.save_paper, url)
    return {"ok": True}
