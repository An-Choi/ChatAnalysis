import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import "./ChatBot.css";

function ChatBot() {
    const [input, setInput] = useState('');
    const [messages, setMessages] = useState([]);
    const chatBoxRef = useRef(null);

    const sendMessage = async (e) => {
        e.preventDefault();
        if (!input.trim()) return;
        const userMessage = input;
        setInput('');
        setMessages([...messages, { from: 'user', text: userMessage }]);
        try {
            const res = await axios.post('http://localhost:8080/api/chat', { message: userMessage });
            setMessages(messages => [...messages, { from: 'chatbot', text: res.data.response }]);
        } catch {
            setMessages(messages => [...messages, { from: 'chatbot', text: '에러가 발생했습니다.' }]);
        }
    };

    useEffect(() => {
        if (chatBoxRef.current)
            chatBoxRef.current.scrollTop = chatBoxRef.current.scrollHeight;
    }, [messages]);

    return (
        <div className="chat-container">
            <div className="chat-header">챗봇 💬</div>
            <div className="chat-messages" ref={chatBoxRef}>
                {messages.map((m, i) => (
                    <div key={i} className={`message ${m.from}`}>
                        {m.text}
                    </div>
                ))}
            </div>
            <form className="chat-input" onSubmit={sendMessage}>
                <input
                    type="text"
                    placeholder="메시지를 입력하세요..."
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    autoComplete="off"
                />
                <button type="submit">전송</button>
            </form>
        </div>
    );
}

export default ChatBot;