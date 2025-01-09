# Mühendislik Öğrencisi Asistanı

Bu uygulama, mühendislik öğrencilerine akademik ve kişisel gelişim konularında destek sağlayan bir chatbot uygulamasıdır.

## Kurulum

### Backend Kurulumu

1. Backend klasörüne gidin:
```bash
cd backend
```

2. Gerekli Python paketlerini yükleyin:
```bash
pip install -r requirements.txt
```

3. `.env` dosyası oluşturun ve OpenAI API anahtarınızı ekleyin:
```
OPENAI_API_KEY=your_api_key_here
```

4. Backend sunucusunu başlatın:
```bash
uvicorn main:app --reload
```

Backend http://localhost:8000 adresinde çalışacaktır.

### Frontend Kurulumu

1. Yeni bir terminal açın ve frontend klasörüne gidin:
```bash
cd frontend
```

2. Frontend'i başlatın:
```bash
python -m http.server 3000
```

Frontend http://localhost:3000 adresinde çalışacaktır.

## Özellikler

- 🎓 Akademik destek
- 💪 Stres yönetimi
- 💡 Problem çözme desteği
- 🤝 Kariyer planlaması
- 💫 Motivasyon desteği
- 🔄 Sohbet geçmişini temizleme
- 💬 Doğal dil işleme
- 🌟 Emoji destekli yanıtlar

## Kullanım

- Web tarayıcınızda http://localhost:3000 adresine gidin
- Mesaj kutusuna sorunuzu veya yorumunuzu yazın
- "Gönder" butonuna tıklayın
- Sohbeti temizlemek için "Sohbeti Temizle" butonunu kullanın

## Gereksinimler

- Python 3.7+
- OpenAI API anahtarı
- Web tarayıcısı 