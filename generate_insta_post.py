
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

SOURCE_TEXT = """
1. 입지 분석: 강남 20분 컷의 진실
제목: 매일 아침 숲속에서 눈뜨고 강남으로 출근한다? 서종 IC 2분 거리의 마법.
썸네일 문구: "강남 30분대 진입? 서종 IC 2분 거리의 진실 공개"
핵심 내용:
Hook: "전원주택은 출퇴근이 불가능하다"는 편견을 깹니다. 꽉 막힌 국도 대신, 집에서 나오자마자 고속도로에 올리는 쾌적함을 상상해 보세요.
Fact: 서울-양양 고속도로 서종 IC까지 단 2분. 강남권 진입까지 물리적 거리를 획기적으로 단축했습니다.
Benefit: 주말 꽉 막힌 양평 도로에 갇혀 보신 적 있나요? 이곳은 IC 바로 앞이라 교통 체증의 스트레스가 없습니다.
Target: 평일엔 강남으로 빠르게 출근하고, 퇴근 후엔 완벽한 숲속 힐링을 원하는 3040 전문직을 위한 최적의 입지입니다
"""

INSTA_PROMPT = f"""
위 내용을 바탕으로 **인스타그램 피드 본문**을 작성해줘.
타겟인 3040 전문직의 감성을 자극하면서도, '강남 출퇴근 가능'이라는 핵심 정보를 명확히 전달해야 해.

[형식 가이드]
1. **첫 줄(헤드라인):** 스크롤을 멈추게 하는 강렬한 한 문장 (이모지 포함)
2. **본문:**
   - 빡빡하지 않게 줄바꿈 자주 사용
   - 핵심 키워드(서종IC 2분, 강남 30분대) 강조
   - 감성적인 문체 ("상상해보세요", "당신의 아침이 달라집니다")
3. **CTA (Call to Action):** "더 자세한 정보는 프로필 링크 확인" 등
4. **해시태그:** 검색량 높은 전원주택 관련 태그 + 양평/서종 지역 태그 + 타겟(직장인, 주말) 태그 믹스해서 15개 이상.

[소스 내용]
{SOURCE_TEXT}
"""

async def generate_insta():
    cookies = load_cookies()
    csrf_token, session_id = await fetch_tokens(cookies)
    auth = AuthTokens(cookies=cookies, csrf_token=csrf_token, session_id=session_id)
    
    async with NotebookLMClient(auth) as client:
        print(f"📱 인스타그램 피드 생성 중... (Notebook ID: {NOTEBOOK_ID})", file=sys.stderr)
        
        result = await client.chat.ask(NOTEBOOK_ID, INSTA_PROMPT)
        
        print("\n" + "="*50)
        print("📸 [인스타그램 피드 초안]")
        print("="*50)
        print(result.answer)
        print("="*50)
        
        # 결과 파일 저장
        with open("insta_post_draft.txt", "w", encoding="utf-8") as f:
            f.write(result.answer)

if __name__ == "__main__":
    asyncio.run(generate_insta())
