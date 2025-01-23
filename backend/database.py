from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# SQLite veritabanı bağlantısı
SQLALCHEMY_DATABASE_URL = "sqlite:///./chatbot.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    user_message = Column(String)
    user_id = Column(Integer, index=True)
    bot_response = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

# Veritabanı tablolarını oluştur
Base.metadata.create_all(bind=engine) 