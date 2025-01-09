from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from chatbot import CustomChatBot
from typing import List, Optional

app = FastAPI(title="Mühendislik Asistanı API")

# CORS ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Güvenlik için production'da spesifik origin'leri belirtin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Sohbet botu örneği
chat_bot = CustomChatBot()

class Message(BaseModel):
    content: str

class ChatResponse(BaseModel):
    response: str
    success: bool
    error: Optional[str] = None

@app.post("/chat", response_model=ChatResponse)
async def chat(message: Message):
    try:
        response = chat_bot.get_response(message.content)
        return ChatResponse(response=response, success=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/clear", response_model=ChatResponse)
async def clear_history():
    try:
        response = chat_bot.clear_history()
        return ChatResponse(response=response, success=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 