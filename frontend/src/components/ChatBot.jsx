import React, { useState } from 'react';
import axios from 'axios';

function ChatBot() {
    const [input, setInput] = useState('');
    const [messages, setMessages] = useState([]);

    const sendMessage = async (e) => {
        e.preventDefault();
        if (!input) return;
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

    return (
        <div>
            <div style={{ minHeight: 160, border: '1px solid #ccc', marginBottom: 10, padding: 10 }}>
                {messages.map((m, i) => (
                    <div key={i} style={{ textAlign: m.from === 'user' ? 'right' : 'left' }}>
                        <b>{m.from === 'user' ? '나' : '챗봇'}:</b> {m.text}
                    </div>
                ))}
            </div>
            <form onSubmit={sendMessage}>
                <input value={input} onChange={e => setInput(e.target.value)} />
                <button type="submit">전송</button>
            </form>
        </div>
    );
}

export default ChatBot;