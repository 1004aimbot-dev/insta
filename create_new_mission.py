
import asyncio
import sys
import os
from notebooklm_mcp.auth import load_cookies
from notebooklm.client import NotebookLMClient
from notebooklm.auth import AuthTokens, fetch_tokens

NEW_TITLE = "Project_Yangpyeong_Eco_Complex_2026"
DESIGN_SPEC_PATH = "d:/yooyk1/notebooklm_mcp/DESIGN_SPEC_15PY.md"
URLS_TO_ADD = [
    "https://m.sentv.co.kr/news/view/677042",
    "https://www.kbthink.com"
]

QUERY_COMMUTE = "서종 IC에서 2분 거리 주택단지에서 서울 강남으로 출퇴근할 때의 장점을 구체적으로 분석해줘. (시간, 비용, 삶의 질 측면)"

async def create_and_analyze():
    cookies = load_cookies()
    csrf_token, session_id = await fetch_tokens(cookies)
    auth = AuthTokens(cookies=cookies, csrf_token=csrf_token, session_id=session_id)
    
    async with NotebookLMClient(auth) as client:
        # 1. 새 노트북 생성
        print(f"🆕 새 노트북 생성 중... ('{NEW_TITLE}')", file=sys.stderr)
        notebook = await client.notebooks.create(title=NEW_TITLE)
        print(f"✅ 생성 완료! ID: {notebook.id}", file=sys.stderr)
        
        # 2. 기존 소스들 이관 (URLs)
        print("📥 자료 이관 중 (URL)...", file=sys.stderr)
        for url in URLS_TO_ADD:
            try:
                await client.sources.add_url(notebook.id, url)
                print(f"  - 추가됨: {url}", file=sys.stderr)
            except Exception as e:
                print(f"  - 실패: {url}", file=sys.stderr)

        # 3. 디자인 스펙 이관 (File)
        print("📥 디자인 스펙 이관 중...", file=sys.stderr)
        try:
             await client.sources.add_file(notebook.id, DESIGN_SPEC_PATH)
             print("  - 추가됨: Design Spec", file=sys.stderr)
        except Exception as e:
             print(f"  - 실패: Design Spec ({e})", file=sys.stderr)

        # 4. 음성 질문(오디오)에 대한 답변 분석
        print(f"🤖 AI 분석 중: '{QUERY_COMMUTE}'", file=sys.stderr)
        ask_result = await client.chat.ask(notebook.id, QUERY_COMMUTE)
        
        print("\n" + "="*50)
        print(f"📍 서종 IC 2분 거리 ➜ 강남 출퇴근 분석")
        print("="*50)
        print(ask_result.answer)
        print("="*50)
        
        # ID 파일로 저장 (나중에 쓰려고)
        with open("current_notebook_id.txt", "w") as f:
            f.write(notebook.id)

if __name__ == "__main__":
    asyncio.run(create_and_analyze())
