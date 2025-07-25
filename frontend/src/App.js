import logo from './logo.svg';
import './App.css';
import React from 'react';
import Home from './pages/Home';
import ChatBot from './components/ChatBot'
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';

function App() {
  return (
    <Router>
      <nav>
        <Link to="/">업로드</Link> | <Link to="/chat">챗봇</Link>
      </nav>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/chat" element={<ChatBot />} />
      </Routes>
    </Router>
  );
}

export default App;
