from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from chatbot import CustomChatBot
from typing import List, Optional
from database import SessionLocal, ChatHistory
from sqlalchemy.orm import Session
from fastapi import Depends

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
    user_id: int
class ChatResponse(BaseModel):
    response: str
    success: bool
    error: Optional[str] = None

# Database bağlantısı için dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/chat", response_model=ChatResponse)
async def chat(message: Message, db: Session = Depends(get_db)):
    try:
        userHistory = db.query(ChatHistory).filter_by(user_id=1).all()
        for history in userHistory:
            print(
                f"ID: {history.id}, "
                f"User ID: {history.user_id}, "
                f"Message: {history.user_message}, "
                f"Response: {history.bot_response}, "
                f"Timestamp: {history.timestamp}"
            )
        response = chat_bot.get_response(message.content)
        
        # Sohbeti veritabanına kaydet
        chat_record = ChatHistory(
            user_message=message.content,
            user_id=1,
            bot_response=response
        )
        db.add(chat_record)
        db.commit()
        
        return ChatResponse(response=response, success=True)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/clear", response_model=ChatResponse)
async def clear_history():
    try:
        response = chat_bot.clear_history()
        return ChatResponse(response=response, success=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 