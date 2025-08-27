FROM node:18-alpine AS build

WORKDIR /app

#package.json + package-lock.json 설치
COPY package*.json ./

#의존성 설치
RUN npm ci --only=production

#소스 코드 복사
COPY . .

RUN npm run build
EXPOSE 3000
CMD ["npx", "serve", "-s", "build", "-l", "3000"]