import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_PROMPT = (
    "You are Aurora, a helpful AI assistant."
)

model = genai.GenerativeModel("models/gemini-2.5-flash")

async def get_chat_response(messages):

    try:

        user_message = messages[-1]["content"]

        prompt = f"""
        {SYSTEM_PROMPT}

        User: {user_message}

        Assistant:
        """

        response = model.generate_content(prompt)

        return {
            "text": response.text
        }

    except Exception as e:

        print("Gemini Error:", e)

        return {
            "error": str(e)
        }