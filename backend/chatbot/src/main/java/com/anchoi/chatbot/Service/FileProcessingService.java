package com.anchoi.chatbot.Service;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.util.HashMap;
import java.util.Map;

import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.multipart.MultipartFile;

@Service
public class FileProcessingService {
    private static final String UPLOAD_DIR = "/app/resources/uploads/";
    private static final String PYTHON_URL = "http://python-server:8000";

    @Async
    public void processFile(MultipartFile file, String jobId) {
        try {
            Path uploadPath = Paths.get(UPLOAD_DIR);
            Files.createDirectories(uploadPath);

            String originalFileName = file.getOriginalFilename();
            String extension = originalFileName.substring(originalFileName.lastIndexOf("."));
            String uniqueFileName = jobId + extension;
            Path filePath = uploadPath.resolve(uniqueFileName);
            Files.copy(file.getInputStream(), filePath, StandardCopyOption.REPLACE_EXISTING);

            RestTemplate restTemplate = new RestTemplate();
            Map<String, String> request = new HashMap<>();
            request.put("filename", uniqueFileName);
            request.put("jobId", jobId);
            request.put("originalFilename", originalFileName);

            restTemplate.postForObject(PYTHON_URL + "/process", request, String.class);
        } catch (IOException e) {
            System.err.println("파일 처리 중 오류: " + e.getMessage());
        }
    }
}
