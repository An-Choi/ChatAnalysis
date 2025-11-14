package com.anchoi.chatbot.Controller;

import java.util.Map;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

import com.anchoi.chatbot.Service.FileProcessingService;

@CrossOrigin(origins = "*")
@RestController
@RequestMapping("/api/v1/files")
public class FileController {

    @Autowired
    private FileProcessingService fileProcessingService;
    private final Map<String, String> jobStatus = new ConcurrentHashMap<>();

    @PostMapping("/upload")
    public ResponseEntity<?> uploadFile(@RequestParam("file") MultipartFile file) {
        if (file.isEmpty()) {
            return ResponseEntity.badRequest().body("파일이 비어 있습니다.");
        }

        String jobId = UUID.randomUUID().toString();
        jobStatus.put(jobId, "PROCESSING");
        fileProcessingService.processFile(file, jobId);
        return ResponseEntity.ok(Map.of("jobId", jobId));
    }

    @GetMapping("/status/{jobId}")
    public ResponseEntity<?> getStatus(@PathVariable String jobId) {
        String status = jobStatus.getOrDefault(jobId, "NOT_FOUND");
        return ResponseEntity.ok(Map.of("status", status));
    }

    @PostMapping("/complete")
    public ResponseEntity<?> completeProcessing(@RequestBody Map<String, String> payload) {
        String jobId = payload.get("jobId");
        String status = payload.get("status");
        if (jobId != null && status != null) {
            jobStatus.put(jobId, status);
            System.out.println("Job " + jobId + " updated to " + status);
            return ResponseEntity.ok().build();
        }
        return ResponseEntity.badRequest().build();
    }
}
