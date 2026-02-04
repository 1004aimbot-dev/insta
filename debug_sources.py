
import asyncio
import sys
from notebooklm_mcp.auth import load_cookies
from notebooklm.client import NotebookLMClient
from notebooklm.auth import AuthTokens, fetch_tokens

NOTEBOOK_ID = "1c584c79-67e0-4fd8-b996-9e1eb4ed214e"

async def list_sources():
    cookies = load_cookies()
    if not cookies:
        print("❌ 쿠키 없음", file=sys.stderr)
        return

    csrf_token, session_id = await fetch_tokens(cookies)
    auth = AuthTokens(cookies=cookies, csrf_token=csrf_token, session_id=session_id)
    
    async with NotebookLMClient(auth) as client:
        print(f"📄 소스 목록 조회 중... (Notebook ID: {NOTEBOOK_ID})", file=sys.stderr)
        sources = await client.sources.list(NOTEBOOK_ID)
        
        for s in sources:
            print(f"- {s.title} (Type: {type(s).__name__}, ID: {s.id})")
            # 속성 검사
            if hasattr(s, 'file_id'):
                print(f"  file_id: {s.file_id}")
            else:
                print(f"  file_id: 없음")

if __name__ == "__main__":
    asyncio.run(list_sources())
