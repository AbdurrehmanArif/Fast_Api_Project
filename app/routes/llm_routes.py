from fastapi import APIRouter, Depends, HTTPException
from app.auth import get_current_user
from app.schemas import LLMRequest, LLMResponse
from app.core.config import settings
import google.generativeai as genai

router = APIRouter(prefix="/llm", tags=["LLM"])

# Configure Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

@router.post("/ask-llm", response_model=LLMResponse)
def ask_llm(payload: LLMRequest, current_user=Depends(get_current_user)):
    try:
        user_prompt = payload.prompt

        # Call Gemini API
        response = model.generate_content(user_prompt)

        return LLMResponse(response=response.text)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))