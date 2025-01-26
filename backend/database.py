from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./chatbot.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()

class ChatHistory(Base):
    __tablename__ = "chat_history"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    user_message = Column(String)
    bot_response = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

# Session handler with yield
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Basic history fetcher
def get_chat_history(user_id, db):
    return db.query(ChatHistory).filter_by(user_id=user_id).order_by(ChatHistory.timestamp).all()