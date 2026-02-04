
import asyncio
import sys
from notebooklm_mcp.auth import load_cookies
from notebooklm.client import NotebookLMClient
from notebooklm.auth import AuthTokens, fetch_tokens

try:
    with open("current_notebook_id.txt", "r") as f:
        NOTEBOOK_ID = f.read().strip()
except FileNotFoundError:
    print("❌ 노트북 ID 파일을 찾을 수 없습니다.", file=sys.stderr)
    sys.exit(1)

ROI_PROMPT = """
이 프로젝트(양평 서종면 15평형 프리미엄 모듈러 주택)의 예상 수익률(ROI)을 시뮬레이션해줘.
현재 업로드된 시장 자료와 디자인 스펙을 바탕으로 합리적인 가정을 하여 계산해줘.

[요청 사항]
1. **비용 추산:**
   - 토지 매입비 (서종면 대지 100평 기준 가정)
   - 건축비 (프리미엄 모듈러, 평당 800~1000만원 가정 시)
   - 부대비용 (인허가, 조경, 마케팅 등)
2. **매출 추산:**
   - 분양가 (주변 시세 및 '호텔급' 프리미엄 반영)
3. **최종 수익률:**
   - 순수익 및 ROI (%)
4. **결론:**
   - 이 사업이 재무적으로 타당한지, 수익률을 높이기 위한 제언.
"""

async def calculate_roi():
    cookies = load_cookies()
    
    try:
        csrf_token, session_id = await fetch_tokens(cookies)
    except Exception as e:
        print(f"⚠️ 저장된 쿠키로 인증 실패: {e}", file=sys.stderr)
        print("🔄 브라우저에서 새 쿠키 추출 시도...", file=sys.stderr)
        from notebooklm_mcp.auth import get_notebooklm_cookies, save_cookies
        cookies = get_notebooklm_cookies("chrome")
        if not cookies:
             print("❌ 쿠키 갱신 실패. 브라우저 로그인이 필요합니다.", file=sys.stderr)
             return
        save_cookies(cookies)
        csrf_token, session_id = await fetch_tokens(cookies)

    auth = AuthTokens(cookies=cookies, csrf_token=csrf_token, session_id=session_id)
    
    async with NotebookLMClient(auth) as client:
        print(f"💰 ROI 시뮬레이션 중... (Notebook ID: {NOTEBOOK_ID})", file=sys.stderr)
        
        result = await client.chat.ask(NOTEBOOK_ID, ROI_PROMPT)
        
        print("\n" + "="*50)
        print("📊 [예상 수익률 분석 리포트]")
        print("="*50)
        print(result.answer)
        print("="*50)
        
        # 파일로 저장 (인코딩 문제 방지용)
        with open("roi_result.txt", "w", encoding="utf-8") as f:
            f.write(result.answer)

if __name__ == "__main__":
    asyncio.run(calculate_roi())
