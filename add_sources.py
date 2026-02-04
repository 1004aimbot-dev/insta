
import asyncio
import sys
from notebooklm_mcp.auth import load_cookies
from notebooklm.client import NotebookLMClient
from notebooklm.auth import AuthTokens, fetch_tokens

NOTEBOOK_ID = "1c584c79-67e0-4fd8-b996-9e1eb4ed214e"

URLS_TO_ADD = [
    "https://m.sentv.co.kr/news/view/677042", # 양평군 주택 정책 관련 뉴스
    "http://www.budongsanmart.co.kr", # 양평 부동산 마트 (참고용 메인)
    "https://www.kbthink.com" # KB 경영연구소 부동신 시장 전망
]

async def add_sources():
    cookies = load_cookies()
    if not cookies:
        print("❌ 쿠키 없음", file=sys.stderr)
        return

    csrf_token, session_id = await fetch_tokens(cookies)
    auth = AuthTokens(cookies=cookies, csrf_token=csrf_token, session_id=session_id)
    
    async with NotebookLMClient(auth) as client:
        print(f"📥 소스 추가 시작 (Notebook ID: {NOTEBOOK_ID})", file=sys.stderr)
        
        for url in URLS_TO_ADD:
            try:
                print(f"   🔗 추가 중: {url}", file=sys.stderr)
                await client.sources.add_url(NOTEBOOK_ID, url)
                print(f"   ✅ 성공: {url}")
            except Exception as e:
                print(f"   ❌ 실패 ({url}): {e}", file=sys.stderr)

if __name__ == "__main__":
    asyncio.run(add_sources())
