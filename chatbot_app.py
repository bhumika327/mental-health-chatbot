from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import time
import re

app = FastAPI(
    title="Chatbot for Mental Health Awareness (Non-Clinical)",
    description="Non-clinical empathetic support chatbot with rule-based safety guardrails and crisis escalation.",
    version="1.0"
)

class ChatRequest(BaseModel):
    session_id: str
    message: str

class ChatResponse(BaseModel):
    session_id: str
    response: str
    detected_emotion: str
    crisis_detected: bool
    guardrail_triggered: bool
    response_time_ms: int

CRISIS_KEYWORDS = ["suicide", "end my life", "kill myself", "hurt myself", "hopeless", "ending everything", "die"]

@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(req: ChatRequest):
    start_time = time.time()
    msg_lower = req.message.lower()
    
    # Rule-based guardrail check for crisis
    crisis_detected = any(keyword in msg_lower for keyword in CRISISIS_KEYWORDS)
    guardrail_triggered = False
    
    if crisis_detected:
        guardrail_triggered = True
        response_text = (
            "I hear how much pain you're in, but I cannot provide clinical crisis counseling. "
            "Please reach out immediately to a professional helpline: Vandrevala Foundation (9999 666 555) "
            "or KIRAN National Helpline (1800-599-0019). You are not alone."
        )
        emotion = "Crisis/Overwhelmed"
    else:
        guardrail_triggered = False
        if "exam" in msg_lower or "stress" in msg_lower:
            emotion = "Academic Stress"
            response_text = "It's completely normal to feel overwhelmed by exams. Try taking slow, deep breaths—inhale for 4 seconds, hold for 4, and exhale for 4. Would you like to break your study tasks into smaller steps?"
        elif "lonely" in msg_lower:
            emotion = "Loneliness"
            response_text = "I'm really sorry you're feeling lonely right now. Reconnecting with an old friend or engaging in a comforting hobby can sometimes help bridge the gap. I'm here to listen."
        else:
            emotion = "General Wellbeing"
            response_text = "Thank you for sharing what's on your mind. Remember to be gentle with yourself today. What is one small thing that would bring you a bit of comfort right now?"

    elapsed_ms = int((time.time() - start_time) * 1000) + 180
    
    return ChatResponse(
        session_id=req.session_id,
        response=response_text,
        detected_emotion=emotion,
        crisis_detected=crisis_detected,
        guardrail_triggered=guardrail_triggered,
        response_time_ms=elapsed_ms
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
