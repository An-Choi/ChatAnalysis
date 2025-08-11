import React, { useState } from 'react';
import axios from 'axios';
import './FileUpload.css'


function FileUpload() {
    const [file, setFile] = useState(null);
    const [message, setMessage] = useState('');

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    };

    const handleUpload = async () => {
        if (!file) {
            setMessage('파일을 선택하세요.');
            return;
        }
        const formData = new FormData();
        formData.append('file', file);
        try {
            const res = await axios.post('http://localhost:8080/api/v1/files/upload', formData);
            setMessage(res.data);
        } catch (err) {
            setMessage('파일 업로드 실패');
        }
    };

    return (
        <div className="upload-container">
            <div className="upload-header">파일 업로드 📁</div>
            <div className="upload-form">
                <input className="upload-input" type="file" onChange={handleFileChange} />
                <button className="upload-btn" onClick={handleUpload}>업로드</button>
            </div>
            {message && (
                <div className={`upload-message ${message === "파일 업로드 실패" ? "error" : "success"}`}>
                    {message}
                </div>
            )}
        </div>
    );
}

export default FileUpload;