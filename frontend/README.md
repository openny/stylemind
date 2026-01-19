# StyleMind

StyleMind는 **블로그 글의 스타일을 분석**하고,  
**사용자가 제공한 이미지와 주제**를 바탕으로  
분석된 스타일을 적용한 **새로운 블로그 포스트를 생성**해주는 AI 어시스턴트 서비스입니다.

---

## 주요 기능

### 1. 스타일 분석 (Style Analysis)
- 블로그 URL 목록을 입력받아 콘텐츠를 크롤링
- 작성자의 글쓰기 스타일, 문체, 톤앤매너 분석
- 블로그 스타일 가이드 프롬프트 생성

### 2. 이미지 분석 (Image Analysis)
- 업로드된 이미지를 AI가 분석
- 이미지에 대한 상세 설명 텍스트 생성

### 3. 맞춤형 포스팅 생성 (Blog Generation)
- 스타일 분석 결과
- 이미지 설명
- 사용자가 입력한 주제  
를 결합하여 최적화된 블로그 포스트 자동 생성

---

## 기술 스택

### Backend
- Python 3.14+
- FastAPI
- Uvicorn

### AI / LLM
- WritingAgent (Custom Agent)
- StyleAnalyzer

### Crawling
- BeautifulSoup4

### Utilities
- asyncio
- Pydantic
- Pillow

---

## 설치 및 실행 방법

### 1. 가상환경 설정 (virtualenv)

```bash
# 가상환경 생성
virtualenv venv

# 가상환경 활성화 (Windows)
# .\venv\Scripts\activate

# 가상환경 활성화 (macOS / Linux)
source venv/bin/activate