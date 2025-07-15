import React, { useState } from 'react';
import axios from 'axios';

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
        <div>
            <h2>파일 업로드</h2>
            <input type="file" onChange={handleFileChange} />
            <button onClick={handleUpload}>업로드</button>
            <p>{message}</p>
        </div>
    );
}

export default FileUpload;