
import asyncio
import sys
from notebooklm_mcp.auth import load_cookies
from notebooklm.client import NotebookLMClient
from notebooklm.auth import AuthTokens, fetch_tokens

async def find_yangpyeong_notebook():
    cookies = load_cookies()
    if not cookies:
        print("❌ 쿠키 없음", file=sys.stderr)
        return

    csrf_token, session_id = await fetch_tokens(cookies)
    auth = AuthTokens(cookies=cookies, csrf_token=csrf_token, session_id=session_id)
    
    async with NotebookLMClient(auth) as client:
        notebooks = await client.notebooks.list()
        
        target_keyword = "Yangpyeong"
        print(f"🔍 '{target_keyword}' 관련 노트북 검색 중...", file=sys.stderr)
        
        found = []
        for nb in notebooks:
            if target_keyword.lower() in nb.title.lower() or "양평" in nb.title:
                print(f"✅ 발견: {nb.title} (ID: {nb.id})")
                found.append(nb)
                
        if not found:
            print("⚠️ 관련 노트북을 찾지 못해 새로 생성합니다...", file=sys.stderr)
            new_nb = await client.notebooks.create(title="Yangpyeong Project Research")
            print(f"🆕 생성 완료: {new_nb.title} (ID: {new_nb.id})")

if __name__ == "__main__":
    asyncio.run(find_yangpyeong_notebook())
