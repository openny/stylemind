FROM python:3.14.0-slim

WORKDIR /app

# 시스템 의존성 설치 (Playwright 브라우저 구동용)
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# requirements.txt 복사 및 설치 (오타 수정: . 앞에 공백 추가)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Playwright 브라우저 설치
RUN playwright install chromium
RUN playwright install-deps chromium

# 소스 코드 복사 (오타 수정: . . 사이에 공백 추가)
COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]