from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from chatbot import CustomChatBot
from typing import List, Optional
from database import SessionLocal, ChatHistory
from sqlalchemy.orm import Session
from datetime import datetime

app = FastAPI(title="Mühendislik Asistanı API")

# CORS ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

chat_bot = CustomChatBot()

class Message(BaseModel):
    content: str
    user_id: int

class ChatResponse(BaseModel):
    response: str
    success: bool
    error: Optional[str] = None

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/get/messages/{user_id}", response_model=List[dict])
async def get_messages(user_id: int, db: Session = Depends(get_db)):
    try:
        messages = db.query(ChatHistory).filter_by(user_id=user_id).all()
        
        return [
            {
                "id": msg.id,
                "user_message": msg.user_message,
                "bot_response": msg.bot_response,
                "timestamp": msg.timestamp.isoformat()
            }
            for msg in messages
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/chat/history/{user_id}", response_model=List[dict])
async def chat_history(user_id: int, db: Session = Depends(get_db)):
    try:
        messages = db.query(ChatHistory).filter_by(user_id=user_id).all()
        return [
            {
                "id": msg.id,
                "user_message": msg.user_message,
                "bot_response": msg.bot_response,
                "timestamp": msg.timestamp.isoformat()
            }
            for msg in messages
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat", response_model=ChatResponse)
async def chat(message: Message, db: Session = Depends(get_db)):
    try:
        user_history = db.query(ChatHistory).filter_by(user_id=message.user_id).all()
        chat_context = "\n".join(
            [f"User: {msg.user_message}\nBot: {msg.bot_response}" 
             for msg in user_history]
        )
        full_message = f"{chat_context}\nUser: {message.content}" if chat_context else message.content
        response = chat_bot.get_response(full_message)
        new_record = ChatHistory(
            user_id=message.user_id,
            user_message=message.content,
            bot_response=response,
            timestamp=datetime.utcnow()
        )
        db.add(new_record)
        db.commit()
        return ChatResponse(response=response, success=True)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/clear/{user_id}", response_model=ChatResponse)
async def clear_history(user_id: int, db: Session = Depends(get_db)):
    try:
        db.query(ChatHistory).filter_by(user_id=user_id).delete()
        db.commit()
        chat_bot.clear_history()
        return ChatResponse(response="Geçmiş temizlendi", success=True)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 