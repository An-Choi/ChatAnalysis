package com.anchoi.chatbot.Controller;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.util.HashMap;
import java.util.Map;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.multipart.MultipartFile;

@CrossOrigin(origins = "*")
@RestController
@RequestMapping("/api/v1/files")
public class FileController {
    private static final String UPLOAD_DIR = "/app/resources/uploads/";
    private static final String PYTHON_URL = "http://python-server:8000";

    @PostMapping("/upload")
    public ResponseEntity<String> uploadFile(@RequestParam("file") MultipartFile file) {
        if (file.isEmpty()) {
            return ResponseEntity.badRequest().body("파일이 비어 있습니다.");
        }
        try {
            // 파일 저장
            Path uploadPath = Paths.get(UPLOAD_DIR);
            if(!Files.exists(uploadPath)) {
                Files.createDirectories(uploadPath);
            }
            String originalFilename = file.getOriginalFilename();
            Path filePath = uploadPath.resolve(originalFilename);
            Files.copy(file.getInputStream(), filePath, StandardCopyOption.REPLACE_EXISTING);

            //데이터 전처리 실행
            RestTemplate restTemplate = new RestTemplate();
            Map<String, String> request = new HashMap<>();
            request.put("filename", originalFilename);

            try {
                ResponseEntity<String> response = restTemplate.postForEntity("http://python-server:8000/process", request,
                        String.class);
                if (response.getStatusCode().is2xxSuccessful()) {
                    return ResponseEntity.ok("파일이 업로드되고 전처리가 완료되었습니다.");
                } else {
                    return ResponseEntity.ok("파일은 업로드되었지만 전처리 중 오류가 발생했습니다.");
                }
            } catch (Exception e) {
                return ResponseEntity.ok("파일이 업로드되었습니다. (전처리 서버 연결 실패)");
            }
        } catch (IOException e) {
            return ResponseEntity.status(500).body("파일 업로드 중 오류가 발생했습니다." + e.getMessage());
        }
    }
}
