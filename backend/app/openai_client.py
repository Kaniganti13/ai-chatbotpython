import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

MODEL_NAME = "models/gemini-flash-latest"

SYSTEM_PROMPT = (
    "You are Aurora, a friendly AI assistant."
)

async def get_chat_response(messages):
    try:
        conversation = "\n".join(
            [f"{m['role']}: {m['content']}" for m in messages]
        )

        prompt = f"{SYSTEM_PROMPT}\n\n{conversation}"

        gemini_model = genai.GenerativeModel(MODEL_NAME)

        response = gemini_model.generate_content(prompt)

        return {"text": response.text}

    except Exception as e:
        print("Gemini Error:", e)
        return {"error": str(e)}