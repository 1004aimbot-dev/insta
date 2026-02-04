
import asyncio
import sys
from datetime import datetime
from notebooklm_mcp.auth import load_cookies
from notebooklm.client import NotebookLMClient
from notebooklm.auth import AuthTokens, fetch_tokens

# ID 파일에서 읽기
try:
    with open("current_notebook_id.txt", "r") as f:
        NOTEBOOK_ID = f.read().strip()
except FileNotFoundError:
    print("❌ 노트북 ID 파일을 찾을 수 없습니다.", file=sys.stderr)
    sys.exit(1)

# 블로그 시리즈 프롬프트
SERIES_PROMPT = """
프로젝트 'The Yangpyeong Solitude' (15평형 프리미엄 모듈러)의 마케팅을 위한 [블로그 포스팅 5부작 시리즈]의 **본문 전체**를 작성해줘.
기획했던 아래 5가지 주제를 이어서 작성하되, 독자가 3040 전문직임을 감안하여 '세련되고 감성적인 문체'로 써줘.
각 포스팅은 [제목], [썸네일 카피], [본문], [해시태그] 형식으로 구분해줘.

[주제]
1. Ep 1. 입지: 강남에서 20분, 나만의 숲을 만나다 (교통/입지)
2. Ep 2. 공간: 15평을 30평처럼 쓰는 마법 (디자인/개방감)
3. Ep 3. 휴식: 퇴근 후, 별을 보며 즐기는 노천탕 (라이프스타일)
4. Ep 4. 관리: 도착 10분 전 보일러를 켜다 (스마트홈/관리비 제로)
5. Ep 5. 기회: 당신의 주말을 소유하세요 (분양 안내/수익성)

반드시 글자수 제한 없이 **상세하게** 작성해줘.
"""

async def generate_blog_series():
    cookies = load_cookies()
    csrf_token, session_id = await fetch_tokens(cookies)
    auth = AuthTokens(cookies=cookies, csrf_token=csrf_token, session_id=session_id)
    
    async with NotebookLMClient(auth) as client:
        print(f"✍️ 블로그 시리즈 집필 중... (Notebook ID: {NOTEBOOK_ID})", file=sys.stderr)
        
        result = await client.chat.ask(NOTEBOOK_ID, SERIES_PROMPT)
        
        # 파일 저장
        output_file = "d:/yooyk1/notebooklm_mcp/BLOG_SERIES_FULL.md"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(f"# 📝 The Yangpyeong Solitude: 블로그 5부작 시리즈\n\n")
            f.write(f"**생성 일시:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
            f.write(result.answer)
            
        print(f"\n✅ 블로그 시리즈 작성 완료: {output_file}", file=sys.stderr)
        
        # 리포트에 통합 (update_report.py 사용 또는 직접 추가)
        # 여기서는 파일 생성만 하고 나중에 통합 스크립트 실행
        
if __name__ == "__main__":
    asyncio.run(generate_blog_series())
