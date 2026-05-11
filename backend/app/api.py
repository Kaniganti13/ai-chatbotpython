# backend/app/api.py
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from .openai_client import get_chat_response, SYSTEM_PROMPT
from typing import Dict, Any, List
from app.chat_history import save_message, load_history
router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def landing_page(request: Request):
    """
    Serve the landing page (index.html).
    Static files are served by FastAPI static mount in main.py.
    """
    # The static index.html will be served by static file mount; this route is optional.
    return HTMLResponse(open("app/static/index.html", "r", encoding="utf-8").read())

@router.get("/chat", response_class=HTMLResponse)
async def chat_page():
    """
    Serve the chat UI page.
    """
    return HTMLResponse(open("app/static/chat.html", "r", encoding="utf-8").read())

@router.post("/api/chat")
async def chat_endpoint(payload: Dict[str, Any]):
    """
    Accepts JSON payload:
    {
      "message": "User message string",
      "history": [ {"role":"user"/"assistant","content":"..."} ]  // optional
    }
    Returns:
    { "reply": "AI reply text" }
    """
    try:
        user_message = payload.get("message", "").strip()
        history = payload.get("history", []) or []

        if not user_message:
            raise HTTPException(status_code=400, detail="Message is empty.")

        # Build messages for OpenAI: include system prompt + history + current user message
        messages: List[Dict[str, str]] = [{"role": "system", "content": SYSTEM_PROMPT}]
        # Append history if provided (client-side history)
        for item in history:
            # Validate structure
            role = item.get("role")
            content = item.get("content")
            if role in ("user", "assistant") and content:
                messages.append({"role": role, "content": content})
        # Append current user message
        messages.append({"role": "user", "content": user_message})

        # Call OpenAI client
        result = await get_chat_response(messages)

        if "error" in result:
            # Return a friendly error message
            return JSONResponse(status_code=500, content={"error": "AI service error: " + result["error"]})

        reply_text = result.get("text", "")
        return {"reply": reply_text}

    except HTTPException as he:
        raise he
    except Exception as e:
        # Generic error
        raise HTTPException(status_code=500, detail=str(e))
