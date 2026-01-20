# StyleMind: AI Blog Post Generator

StyleMind는 사용자의 글쓰기 스타일을 분석하고, 시각적 요소를 파악하여 맞춤형 블로그 포스팅을 생성하는 AI 서비스입니다. vLLM을 통해 최신 LLM(Qwen2.5) 및 Vision 모델을 로컬 환경에서 구동합니다.

## 🚀 주요 기능

- **Style Analysis**: 특정 블로그 URL들을 분석하여 작성자 특유의 문체와 톤앤매너 추출
- **Vision Recognition**: 업로드된 이미지를 Qwen2.5-VL 모델로 분석하여 상세 묘사 생성
- **AI Writing**: 분석된 스타일과 이미지 정보를 결합하여 고품질의 블로그 본문 자동 작성
- **Full-Stack Solution**: React 프론트엔드와 FastAPI 백엔드, 그리고 GPU 가속 AI 모델 서버 통합

## 🛠 기술 스택

- **Frontend**: React (Vite), Tailwind CSS
- **Backend**: FastAPI (Python 3.14), Playwright (크롤링)
- **AI Serving**: vLLM (OpenAI Compatible API)
- **Models**: 
  - Text: `Qwen/Qwen2.5-32B-Instruct-AWQ`
  - Vision: `Qwen/Qwen2.5-VL-7B-Instruct-AWQ`
- **Infrastructure**: Docker, Docker Compose, NVIDIA Container Toolkit

## 📋 사전 준비 사항

- **GPU**: NVIDIA GPU (VRAM 24GB 이상 권장)
- **Software**: Docker, Docker Compose, NVIDIA Container Toolkit 설치
- **HF Token**: Hugging Face 모델 다운로드를 위한 `HF_TOKEN` 필요

## ⚙️ 시작하기 (Docker Compose)

1. **환경 변수 설정**
   `.env` 파일을 생성하고 Hugging Face 토큰을 입력합니다.
   ```bash
   HF_TOKEN=your_huggingface_token_here
   ```

2. **서비스 실행**
   ```bash
   docker-compose up -d
   ```
   *참고: 모델 다운로드 및 GPU 모델 로드에 시간이 소요될 수 있습니다.*

3. **접속 정보**
   - **Frontend**: `http://localhost:3000`
   - **Backend API**: `http://localhost:8080`
   - **Text Model API**: `http://localhost:8000`
   - **Vision Model API**: `http://localhost:8001`

## 🏗 프로젝트 구조

- `/frontend`: React 기반 사용자 인터페이스
- `/backend`: FastAPI 서버 및 비즈니스 로직
- `docker-compose.yml`: vLLM 서버 및 앱 서비스 오케스트레이션
- `Dockerfile`: 백엔드 실행을 위한 Playwright 및 종속성 설정

## ⚠️ 주의 사항

- 본 프로젝트는 GPU 가속을 사용하므로 Docker 환경에서 `nvidia-runtime`이 활성화되어 있어야 합니다.
- `vllm-text` 서비스는 약 0.65의 GPU 메모리 점유율을, `vllm-vision`은 0.25를 사용하도록 설정되어 있습니다. 사용자의 하드웨어 환경에 따라 `docker-compose.yml`의 `gpu-memory-utilization` 값을 조절하세요.