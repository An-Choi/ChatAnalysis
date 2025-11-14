import logo from "./logo.svg";
import "./App.css";
import React from "react";
import Home from "./pages/Home";
import ChatBot from "./components/ChatBot";
import Loading from "./components/Loading";
import FileUpload from "./components/FileUpload";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";

function App() {
  return (
    <Router>
      <nav>
        <Link to="/">업로드</Link> | <Link to="/chat">챗봇</Link>
      </nav>
      <Routes>
        <Route path="/" element={<FileUpload />} />
        <Route path="/chat" element={<ChatBot />} />
        <Route path="/loading" element={<Loading />} />
      </Routes>
    </Router>
  );
}

export default App;
