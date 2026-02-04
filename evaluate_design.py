
import asyncio
import sys
import os
import tempfile
from notebooklm_mcp.auth import load_cookies
from notebooklm.client import NotebookLMClient
from notebooklm.auth import AuthTokens, fetch_tokens

NOTEBOOK_ID = "1c584c79-67e0-4fd8-b996-9e1eb4ed214e"
DESIGN_SPEC_PATH = "d:/yooyk1/notebooklm_mcp/DESIGN_SPEC_15PY.md"
QUERY = "이 디자인 설계안이 앞서 제안한 3040 타겟 전략 및 '관리비 제로' 목표에 얼마나 부합하는지 평가해줘. 그리고 추가적으로 보완할 점이 있다면 알려줘."

async def evaluate_design():
    cookies = load_cookies()
    if not cookies:
        print("❌ 쿠키 없음", file=sys.stderr)
        return

    csrf_token, session_id = await fetch_tokens(cookies)
    auth = AuthTokens(cookies=cookies, csrf_token=csrf_token, session_id=session_id)
    
    async with NotebookLMClient(auth) as client:
        # 1. 파일 업로드 (MD 파일을 텍스트 파일로 인식시켜 업로드)
        print(f"📤 디자인 스펙 업로드 중... ({DESIGN_SPEC_PATH})", file=sys.stderr)
        
        # notebooklm 라이브러리는 파일 경로를 받아 업로드함.
        # .md 확장자를 잘 처리하는지 확인 안되었으나 텍스트 기반이므로 시도.
        try:
             await client.sources.add_file(NOTEBOOK_ID, DESIGN_SPEC_PATH)
             print("✅ 업로드 완료", file=sys.stderr)
        except Exception as e:
             print(f"❌ 업로드 실패: {e}", file=sys.stderr)
             return

        # 2. 질문하기
        print(f"🤖 AI 평가 요청 중... (질문: {QUERY})", file=sys.stderr)
        ask_result = await client.chat.ask(NOTEBOOK_ID, QUERY)
        
        print("\n" + "="*50)
        print("📝 디자인 평가 결과")
        print("="*50)
        print(ask_result.answer)
        print("="*50)

if __name__ == "__main__":
    asyncio.run(evaluate_design())
