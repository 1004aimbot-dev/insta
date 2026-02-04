
import asyncio
import sys
from notebooklm_mcp.auth import get_notebooklm_cookies, load_cookies, save_cookies 
from notebooklm.client import NotebookLMClient
from notebooklm.auth import AuthTokens, fetch_tokens

async def list_notebooks():
    print("🍪 쿠키 가져오는 중...", file=sys.stderr)
    # 1. 파일에서 먼저 로드 시도 (수동 저장된 것 사용 위해)
    cookies = load_cookies()
    if not cookies:
        print("⚠️ 저장된 쿠키 없음, 브라우저 추출 시도...", file=sys.stderr)
        cookies = get_notebooklm_cookies("chrome")
    
    if not cookies:
        print("❌ 쿠키 실패", file=sys.stderr)
        return

    print("🔐 토큰 교환 중...", file=sys.stderr)
    try:
        csrf_token, session_id = await fetch_tokens(cookies)
        auth = AuthTokens(cookies=cookies, csrf_token=csrf_token, session_id=session_id)
        
        async with NotebookLMClient(auth) as client:
            print("📚 노트북 목록 조회 중...", file=sys.stderr)
            notebooks = await client.notebooks.list()
            
            print("\n" + "="*50)
            print(f"   📋 내 NotebookLM 목록 (총 {len(notebooks)}개)")
            print("="*50)
            for i, nb in enumerate(notebooks, 1):
                # nb 객체의 속성 확인 (title, id 등)
                title = getattr(nb, 'title', '제목 없음')
                nb_id = getattr(nb, 'id', 'ID 없음')
                print(f"{i}. {title}")
                print(f"   🔗 ID: {nb_id}")
                print("-" * 50)
                
    except Exception as e:
        print(f"❌ 오류 발생: {e}", file=sys.stderr)

if __name__ == "__main__":
    asyncio.run(list_notebooks())
