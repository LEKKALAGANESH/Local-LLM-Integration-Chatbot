import axios from 'axios';
import { useEffect, useRef, useState } from 'react';
import './App.css';

function App() {
  const [message, setMessage] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const chatHistoryRef = useRef(null);

  const sendMessage = async () => {
    if (!message.trim()) return;

    setLoading(true);
    const userMessage = { role: 'user', content: message };
    setChatHistory(prev => [...prev, userMessage]);

    try {
      const response = await axios.post('http://localhost:8000/chat', { query: message });
      const botMessage = { role: 'bot', content: response.data.response };
      setChatHistory(prev => [...prev, botMessage]);
    } catch (error) {
      const errorMessage = { role: 'bot', content: 'Error: Could not connect to the chatbot. Make sure the backend is running.' };
      setChatHistory(prev => [...prev, errorMessage]);
    }

    setMessage('');
    setLoading(false);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  useEffect(() => {
    if (chatHistoryRef.current) {
      chatHistoryRef.current.scrollTop = chatHistoryRef.current.scrollHeight;
    }
  }, [chatHistory]);

  return (
    <div className="App">
      <header className="App-header">
        <h1>🍳 Recipe Chatbot</h1>
        <p>Tell me your ingredients, and I'll suggest recipes!</p>
      </header>
      <div className="chat-container">
        <div className="chat-history" ref={chatHistoryRef}>
          {chatHistory.length === 0 && (
            <div className="message bot" style={{ margin: 'auto', maxWidth: '100%', textAlign: 'center', opacity: 0.7 }}>
              👋 Hi! I'm your recipe assistant. Try entering ingredients like "egg, onion" or ask me anything!
            </div>
          )}
          {chatHistory.map((msg, index) => (
            <div key={index} className={`message ${msg.role}`}>
              {msg.content}
            </div>
          ))}
          {loading && (
            <div className="message bot">
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <div className="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
                Thinking...
              </div>
            </div>
          )}
        </div>
        <div className="input-container">
          <input
            type="text"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Enter ingredients or ask a question..."
            disabled={loading}
          />
          <button onClick={sendMessage} disabled={loading || !message.trim()}>
            Send
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;
