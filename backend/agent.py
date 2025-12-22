import base64
import io
import os

from PIL import Image
from openai import AsyncOpenAI


class WritingAgent:
    def __init__(self):
        # Docker Compose에서 설정한 환경변수를 사용하여 서비스 간 통신 주소 설정
        text_url = os.getenv("TEXT_MODEL_URL", "http://localhost:8356/v1")
        vision_url = os.getenv("VISION_MODEL_URL", "http://localhost:8357/v1")

        self.text_client = AsyncOpenAI(api_key="EMPTY", base_url=text_url)
        self.vision_client = AsyncOpenAI(api_key="EMPTY", base_url=vision_url)

        self.text_model = "qwen2.5-32b-awq"
        self.vision_model = "qwen2.5-vl-7b-awq"
    async def analyze_image_url(self, image_url):
        """이미지 URL을 직접 사용하여 내용을 분석합니다."""
        response = await self.vision_client.chat.completions.create(
            model=self.vision_model,
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": "이 이미지의 상황, 분위기, 주요 객체를 한국어로 매우 상세하게 묘사해줘."},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_url
                        }
                    }
                ]
            }]
        )
        return response.choices[0].message.content

    async def analyze_image(self, base64_image, mime_type="image/jpeg"):
        # 이미지 크기 최적화 (토큰 절약 및 에러 방지)
        img_data = base64.b64decode(base64_image)
        img = Image.open(io.BytesIO(img_data))

        # 최대 해상도 제한 (예: 1024px)
        if max(img.size) > 1024:
            img.thumbnail((1024, 1024))
            output = io.BytesIO()
            img.save(output, format="JPEG", quality=85)
            base64_image = base64.b64encode(output.getvalue()).decode('utf-8')
            mime_type = "image/jpeg"

        # 정확한 MIME 타입을 포함한 Data URL 생성
        image_url = f"data:{mime_type};base64,{base64_image}"

        response = await self.vision_client.chat.completions.create(
            model=self.vision_model,
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": "이 이미지의 상황, 분위기, 주요 객체를 한국어로 매우 상세하게 묘사해줘."},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_url
                        }
                    }
                ]
            }]
        )
        return response.choices[0].message.content

    async def write_blog(self, topic, image_desc, style_guide):
        prompt = f"""
        당신은 전문 블로거입니다. 아래 스타일 가이드와 이미지 설명을 바탕으로 '{topic}'에 대한 블로그 글을 작성하세요.

        {style_guide}

        [이미지 내용]
        {image_desc}

        [요청사항]
        - 이미지의 내용을 글 중간에 자연스럽게 녹여내세요.
        - 서론-본론-결론 구조를 갖추세요.
        """

        response = await self.text_client.chat.completions.create(
            model=self.text_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=2048
        )
        return response.choices[0].message.content