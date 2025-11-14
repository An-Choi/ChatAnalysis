import React, { use, useEffect, useState } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import axios from "axios";
import "./Loading.css";

function Loading() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const jobId = searchParams.get("jobId");
  const [statusMessage, setStatusMessage] =
    useState("대화 내용 분석을 시작합니다...");

  useEffect(() => {
    if (!jobId) {
      navigate("/");
      return;
    }

    const interval = setInterval(async () => {
      try {
        const res = await axios.get(
          `http://localhost:8080/api/v1/files/status/${jobId}`
        );
        const { status } = res.data;

        if (status == "COMPLETED") {
          clearInterval(interval);
          setStatusMessage("분석 완료! 채팅방으로 이동합니다.");
          setTimeout(() => navigate("/chat"), 1500);
        } else if (status == "FAILED") {
          clearInterval(interval);
          setStatusMessage("오류가 발생했습니다. 다시 시도해주세요.");
          setTimeout(() => navigate("/"), 3000);
        } else {
          setStatusMessage("대화 내용 분석 진행 중...");
        }
      } catch (err) {
        clearInterval(interval);
        setStatusMessage("상태 확인 중 오류가 발생했습니다.");
      }
    }, 3000);
    return () => clearInterval(interval);
  }, [jobId, navigate]);
  return (
    <div className="loading-container">
      <div className="spinner"></div>
      <p>{statusMessage}</p>
    </div>
  );
}

export default Loading;
