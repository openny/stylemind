import asyncio
import base64
import os
import traceback
import uuid
from pathlib import Path
from typing import List

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

from crawler import BlogCrawler
from analyzer import StyleAnalyzer
from agent import WritingAgent

app = FastAPI(title="StyleMind API")

UPLOAD_DIR = "/tmp/stylemind_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 서비스 싱글톤 인스턴스화
crawler = BlogCrawler()
analyzer = StyleAnalyzer()
agent = WritingAgent()


class UrlList(BaseModel):
    urls: List[str]


@app.get("/")
async def root():
    return {"message": "StyleMind Backend is running"}


@app.post("/api/analyze-style")
async def analyze_style(data: UrlList):
    # asyncio.gather를 사용하여 병렬로 여러 URL 크롤링
    tasks = [crawler.get_content(url) for url in data.urls]
    contents = await asyncio.gather(*tasks)

    # 유효한 텍스트만 결합
    full_text = " ".join(filter(None, contents))

    analysis = analyzer.analyze(full_text)
    if not analysis:
        return {"status": "error", "message": "분석할 텍스트를 찾지 못했습니다. URL을 확인해주세요."}

    return {"status": "success", "result": analysis}


@app.post("/api/generate-post")
async def generate_post(
    topic: str = Form(...),
    style_prompt: str = Form(...),
    image: UploadFile = File(...),
):
    try:
        raw = await image.read()
        if not raw:
            raise HTTPException(status_code=400, detail="Empty image upload")

        # 이미지를 Base64로 인코딩
        base64_image = base64.b64encode(raw).decode('utf-8')
        mime_type = image.content_type or "image/jpeg"

        # ✅ URL 방식 대신 Base64 데이터를 직접 전달하여 분석
        image_desc = await agent.analyze_image(base64_image, mime_type)

        content = await agent.write_blog(topic, image_desc, style_prompt)
        return {"content": content, "image_desc": image_desc}

    except HTTPException as e:
        print("HTTPException:", e.detail)
        raise

    except Exception as e:
        print("Exception:", repr(e))
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    # 로컬 테스트 실행용 (uvicorn main:app --host 0.0.0.0 --port 8080)
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)