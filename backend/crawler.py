from playwright.async_api import async_playwright
import asyncio
import sys


class BlogCrawler:
    def __init__(self):
        self._browser_installed = False

    async def _ensure_browser_installed(self):
        """Playwright 브라우저가 설치되어 있는지 확인하고 없으면 설치합니다."""
        if self._browser_installed:
            return

        try:
            # 브라우저 실행 파일이 없는 경우를 대비해 설치 명령을 실행합니다.
            process = await asyncio.create_subprocess_exec(
                sys.executable, "-m", "playwright", "install", "chromium",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await process.communicate()
            self._browser_installed = True
        except Exception as e:
            print(f"Playwright 브라우저 설치 시도 중 오류 발생: {e}")

    async def get_content(self, url: str) -> str:
        # 크롤링 시작 전 브라우저 설치 확인
        await self._ensure_browser_installed()

        async with async_playwright() as p:
            try:
                browser = await p.chromium.launch(headless=True)
                # 봇 탐지 회피를 위한 User-Agent 설정
                context = await browser.new_context(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                )
                page = await context.new_page()

                await page.goto(url, wait_until="networkidle", timeout=30000)
                content = ""

                if "blog.naver.com" in url:
                    # 네이버 블로그는 mainFrame iframe 안에 본문이 있음
                    try:
                        # iframe 로드 대기
                        frame = page.frame_locator("#mainFrame")
                        # 스마트에디터 ONE 컨테이너 대기
                        await frame.locator(".se-main-container").wait_for(timeout=5000)
                        content = await frame.locator(".se-main-container").inner_text()
                    except:
                        # 구형 에디터 폴백
                        try:
                            frame = page.frame_locator("#mainFrame")
                            content = await frame.locator("#postViewArea").inner_text()
                        except:
                            print("네이버 블로그 본문 추출 실패")

                elif "tistory.com" in url:
                    # 티스토리의 다양한 본문 클래스 시도
                    selectors = [".contents_style", ".tt_article_useless_p_margin", "div[class*='article']"]
                    for sel in selectors:
                        if await page.locator(sel).count() > 0:
                            content = await page.locator(sel).first.inner_text()
                            break

                await browser.close()
                return content.strip()

            except Exception as e:
                print(f"Error crawling {url}: {str(e)}")
                return ""