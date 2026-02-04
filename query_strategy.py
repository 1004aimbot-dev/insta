
import asyncio
import sys
from notebooklm_mcp.auth import load_cookies
from notebooklm.client import NotebookLMClient
from notebooklm.auth import AuthTokens, fetch_tokens

NOTEBOOK_ID = "1c584c79-67e0-4fd8-b996-9e1eb4ed214e"
QUERY = "이 소스들을 바탕으로 2026년 양평 서종면 소형 주택 분양 전략을 제안해줘. 특히 타겟 고객층과 차별화 포인트, 마케팅 채널 위주로."

async def query_strategy():
    cookies = load_cookies()
    if not cookies:
        print("❌ 쿠키 없음", file=sys.stderr)
        return

    csrf_token, session_id = await fetch_tokens(cookies)
    auth = AuthTokens(cookies=cookies, csrf_token=csrf_token, session_id=session_id)
    
    async with NotebookLMClient(auth) as client:
        print(f"🤖 AI 분석 요청 중... (질문: {QUERY})", file=sys.stderr)
        
        # chat.ask returns AskResult
        # attributes: answer, conversation_id, etc.
        ask_result = await client.chat.ask(NOTEBOOK_ID, QUERY)
        
        print("\n" + "="*50)
        print("📊 AI 분양 전략 제안")
        print("="*50)
        print(ask_result.answer)
        print("="*50)

if __name__ == "__main__":
    asyncio.run(query_strategy())
