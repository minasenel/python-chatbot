const { useState, useEffect, useRef } = React;

function App() {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef(null);

    // Load chat history on component mount
    useEffect(() => {
        const loadHistory = async () => {
            try {
                console.log('Geçmiş mesajlar yükleniyor...');
                const response = await fetch('http://localhost:8000/chat/history/1');
                const data = await response.json();
                if (data.history) {
                    console.log('Yüklenen geçmiş:', data.history);
                    const historyMessages = data.history.flatMap(item => [
                        { 
                            role: 'user', 
                            content: item.user_message,
                            timestamp: item.timestamp 
                        },
                        { 
                            role: 'assistant', 
                            content: item.bot_response,
                            timestamp: item.timestamp 
                        }
                    ]);
                    setMessages(historyMessages);
                } else {
                    console.log('Geçmiş mesaj bulunamadı.');
                }
            } catch (error) {
                console.error('Error loading history:', error);
            }
        };
        loadHistory();
    }, []);

    useEffect(() => {
        const savedMessages = localStorage.getItem('chatHistory');
        if (savedMessages) {
            console.log('LocalStorage\'dan yüklenen mesajlar:', JSON.parse(savedMessages));
            setMessages(JSON.parse(savedMessages));
        }
    }, []);

    useEffect(() => {
        console.log('LocalStorage\'a kaydedilen mesajlar:', messages);
        localStorage.setItem('chatHistory', JSON.stringify(messages));
    }, [messages]);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const sendMessage = async (e) => {
        e.preventDefault();
        if (!input.trim()) return;

        const userMessage = input;
        setInput('');
        setMessages(prev => [...prev, { 
            role: 'user', 
            content: userMessage,
            timestamp: new Date().toISOString() 
        }]);
        setIsLoading(true);

        try {
            const response = await fetch('http://localhost:8000/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ content: userMessage, user_id: 1 }),
            });

            const data = await response.json();
            if (data.success) {
                setMessages(prev => [...prev, { 
                    role: 'assistant', 
                    content: data.response,
                    timestamp: new Date().toISOString()
                }]);
                console.log('API yanıtı:', data);
                console.log('Güncellenen mesajlar:', messages);
            } else {
                throw new Error(data.error || 'Bir hata oluştu');
            }
        } catch (error) {
            console.error('Error:', error);
            setMessages(prev => [...prev, { 
                role: 'assistant', 
                content: '❌ Üzgünüm, bir hata oluştu. Lütfen tekrar deneyin.',
                timestamp: new Date().toISOString()
            }]);
        } finally {
            setIsLoading(false);
        }
    };

    const clearChat = async () => {
        try {
            const response = await fetch('http://localhost:8000/clear', {
                method: 'POST',
            });
            const data = await response.json();
            if (data.success) {
                setMessages([]);
            }
        } catch (error) {
            console.error('Error clearing chat:', error);
        }
    };

    return (
        <div className="container mx-auto p-4 max-w-4xl">
            <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
                <h1 className="text-3xl font-bold text-center text-blue-600 mb-2">
                    🎓 Mühendislik Öğrencisi Asistanı
                </h1>
                <p className="text-center text-gray-600">
                    Akademik ve kişisel gelişim yolculuğunda yanındayım!
                </p>
            </div>

            <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
                <div className="space-y-4 mb-4 h-96 overflow-y-auto">
                    {messages.map((message, index) => (
                        <div
                            key={index}
                            className={`p-4 rounded-lg relative ${
                                message.role === 'user'
                                    ? 'bg-blue-100 ml-12'
                                    : 'bg-gray-100 mr-12'
                            }`}
                        >
                            <div className="flex justify-between items-center mb-1">
                                <div className="font-bold">
                                    {message.role === 'user' ? '👤 Sen' : '🤖 Asistan'}
                                </div>
                                <div className="text-sm text-timestamp">
                                    {new Date(message.timestamp).toLocaleTimeString('tr-TR', {
                                        hour: '2-digit',
                                        minute: '2-digit'
                                    })}
                                </div>
                            </div>
                            <div className="text-gray-700">{message.content}</div>
                        </div>
                    ))}
                    {isLoading && (
                        <div className="text-center text-gray-500">
                            <div className="animate-pulse">Düşünüyorum... 🤔</div>
                        </div>
                    )}
                    <div ref={messagesEndRef} />
                </div>

                <form onSubmit={sendMessage} className="flex gap-2">
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder="Mesajınızı yazın..."
                        className="flex-1 p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
                        disabled={isLoading}
                    />
                    <button
                        type="submit"
                        disabled={isLoading}
                        className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors disabled:bg-blue-300"
                    >
                        Gönder
                    </button>
                </form>
            </div>

            <div className="text-center">
                <button
                    onClick={clearChat}
                    className="bg-gray-200 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-300 transition-colors"
                >
                    🧹 Sohbeti Temizle
                </button>
            </div>
        </div>
    );
}

const root = document.getElementById('root');
ReactDOM.render(<App />, root); 