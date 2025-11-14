FROM eclipse-temurin:24-jdk

WORKDIR /app

#Maven Wrapper + pom.xml 복사
COPY mvnw .
COPY .mvn .mvn
COPY pom.xml .

#Dependency 다운로드
RUN ./mvnw dependency:go-offline

#소스 코드 복사
COPY src src

RUN ./mvnw clean package -DskipTests

RUN mkdir -p /app/uploads

EXPOSE 8080
CMD ["java", "-jar", "target/chatbot-0.0.1-SNAPSHOT.jar"]
