import openai
from typing import List
import os
from dotenv import load_dotenv
import random

# .env dosyasından API anahtarını yükle
load_dotenv()

# OpenAI API anahtarını ayarla
openai.api_key = os.getenv("OPENAI_API_KEY")

class CustomChatBot:
    def __init__(self, system_prompt: str = None):
        # Emoji koleksiyonları
        self.mood_emojis = ["🎓", "💪", "🌟", "✨", "💫", "🔧", "💡", "🎯", "🚀", "⭐"]
        self.response_emojis = {
            'destek': ["💪", "🤗", "🌟", "✨", "🎯", "💝", "💫", "🌈"],
            'akademik': ["📚", "💡", "🎓", "✏️", "📝", "🔬", "💻", "📊"],
            'motivasyon': ["🚀", "💪", "🎯", "🏆", "⭐", "💯", "🔥", "✨"],
            'problem_çözme': ["🔧", "🛠️", "💡", "🎯", "🔍", "⚡", "💭", "📐"]
        }
        
        default_prompt = f"""Merhaba! Ben mühendislik öğrencilerinin en yakın arkadaşı! {random.choice(self.mood_emojis)}

        Neler yapabilirim:
        🎓 Derslerinde ve projelerinde sana yardımcı olurum
        💪 Stres ve kaygılarınla başa çıkmanda destek olurum
        💡 Problem çözme becerilerini geliştirmene yardım ederim
        🤝 Kariyer planlaması konusunda yol gösteririm
        💫 Motivasyonunu yüksek tutmana destek olurum
        
        Hem akademik hem de kişisel gelişiminde yanındayım! Beraber çalışmak, konuşmak, dertleşmek için buradayım. 
        Ne düşünüyorsun, neye ihtiyacın var? Anlat bakalım! {random.choice(self.mood_emojis)}"""
        
        self.conversation_history: List[dict] = [
            {
                "role": "system",
                "content": system_prompt if system_prompt else default_prompt
            }
        ]

    def add_random_emoji(self, text: str) -> str:
        """Metne uygun emoji ekler"""
        emoji = random.choice(self.mood_emojis)
        return f"{text} {emoji}"

    def clear_history(self):
        system_prompt = self.conversation_history[0]
        self.conversation_history = [system_prompt]
        return self.add_random_emoji("Sohbet geçmişini temizledim! Yeni bir konuya geçebiliriz!")

    def get_response(self, user_input: str) -> str:
        self.conversation_history.append({"role": "user", "content": user_input})
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=self.conversation_history,
                temperature=0.85,
                max_tokens=1000
            )
            
            assistant_response = response.choices[0].message["content"]
            
            # Yanıta uygun kategori seçimi
            if "matematik" in user_input.lower() or "fizik" in user_input.lower() or "ders" in user_input.lower():
                category = 'akademik'
            elif "stres" in user_input.lower() or "yorgun" in user_input.lower() or "bunaldım" in user_input.lower():
                category = 'destek'
            elif "nasıl" in user_input.lower() or "problem" in user_input.lower() or "çözüm" in user_input.lower():
                category = 'problem_çözme'
            else:
                category = 'motivasyon'

            if not any(emoji in assistant_response for category in self.response_emojis.values() for emoji in category):
                assistant_response = f"{random.choice(self.response_emojis[category])} {assistant_response}"
            
            self.conversation_history.append({"role": "assistant", "content": assistant_response})
            
            return assistant_response

        except Exception as e:
            return self.add_random_emoji(f"Bir sorun oluştu dostum, tekrar dener misin? Hata: {str(e)}") 