import openai
import time
from typing import List
import os
from dotenv import load_dotenv

# .env dosyasından API anahtarını yükle
load_dotenv()

# OpenAI API anahtarını ayarla
openai.api_key = os.getenv("OPENAI_API_KEY")

class ClimateChat:
    def __init__(self):
        self.conversation_history: List[dict] = [
            {
                "role": "system",
                "content": """Sen matematik
        
     konusunda uzman bir asistansın. 
                Bilimsel gerçeklere dayalı, açık ve anlaşılır bilgiler ver. 
                İstatistikler ve araştırma sonuçlarıyla desteklenmiş yanıtlar sun. basit ve anlaşılır bir dilde ve emojiler kullanarak
                Kullanıcıları harekete geçmeye teşvik et."""
            }
        ]

    def clear_history(self):
        # Sistem promptunu koruyarak geçmişi temizle
        system_prompt = self.conversation_history[0]
        self.conversation_history = [system_prompt]

    def get_response(self, user_input: str) -> str:
        # Kullanıcı mesajını geçmişe ekle
        self.conversation_history.append({"role": "user", "content": user_input})
        
        try:
            # ChatGPT'den yanıt al
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=self.conversation_history,
                temperature=0.7,
                max_tokens=500
            )
            
            # Asistan yanıtını al ve geçmişe ekle
            assistant_response = response.choices[0].message["content"]
            self.conversation_history.append({"role": "assistant", "content": assistant_response})
            
            return assistant_response

        except Exception as e:
            return f"Üzgünüm, bir hata oluştu: {str(e)}"

def main():
    print("Küresel Isınma Sohbet Asistanı'na Hoş Geldiniz!")
    print("Çıkmak için 'quit' yazın.\n")
    
    chat = ClimateChat()
    
    while True:
        user_input = input("\nSoru veya yorumunuz: ")
        
        if user_input.lower() == 'quit':
            print("\nGörüşmek üzere! Gezegenimizi korumayı unutmayın! 🌍")
            break
            
        response = chat.get_response(user_input)
        print("\nAsistan:", response)
        time.sleep(1)  # Doğal bir sohbet akışı için kısa bekleme

if __name__ == "__main__":
    main() 