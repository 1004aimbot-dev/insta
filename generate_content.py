
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
    print("❌ 노트북 ID 파일을 찾을 수 없습니다. 이전 단계가 완료되었나요?", file=sys.stderr)
    sys.exit(1)

BLOG_PROMPT = """
아래 주제로 블로그 포스팅 5개 세트의 '제목'과 '핵심 내용(썸네일 문구 포함)'을 작성해줘.
타겟: 강남 출퇴근 가능한 전원주택을 찾는 3040 전문직.
컨셉: '서종 IC 2분 거리', '호텔보다 편한 관리비 0원 주택'.
톤앤매너: 감성적이지만 정보는 확실하게.

[포스팅 주제]
1. 입지 분석 (강남 20분 컷의 진실)
2. 디자인 공개 (호텔 같은 15평)
3. 경제성 분석 (관리비 0원의 비밀)
4. 라이프스타일 (퇴근 후 노천탕)
5. 분양 안내 (선착순 혜택)
"""

PLAN_PROMPT = """
이 프로젝트의 '사업계획서(Business Plan) PDF'를 만들기 위한 목차와 페이지별 핵심 내용을 작성해줘.
투자자에게 어필할 수 있도록 '수익성'과 '시장성'을 강조해줘.
"""

async def generate_marketing_content():
    cookies = load_cookies()
    csrf_token, session_id = await fetch_tokens(cookies)
    auth = AuthTokens(cookies=cookies, csrf_token=csrf_token, session_id=session_id)
    
    async with NotebookLMClient(auth) as client:
        print(f"🤖 콘텐츠 생성 중... (Notebook ID: {NOTEBOOK_ID})", file=sys.stderr)
        
        # 1. 블로그 포스팅 생성
        print("📝 블로그 포스팅 5종 세트 작성 중...", file=sys.stderr)
        blog_result = await client.chat.ask(NOTEBOOK_ID, BLOG_PROMPT)
        print("✅ 블로그 초안 완료", file=sys.stderr)
        
        # 2. 사업계획서 초안 생성
        print("📑 사업계획서 초안 작성 중...", file=sys.stderr)
        plan_result = await client.chat.ask(NOTEBOOK_ID, PLAN_PROMPT)
        print("✅ 사업계획서 초안 완료", file=sys.stderr)

        # 결과 모음
        report_content = f"# 📢 프로젝트 마케팅 리포트\n\n"
        report_content += f"**생성 일시:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        report_content += f"**Notebook ID:** {NOTEBOOK_ID}\n\n"
        
        report_content += "## 1. 📝 블로그 마케팅 패키지 (5종)\n\n"
        report_content += blog_result.answer + "\n\n"
        
        report_content += "---\n\n"
        
        report_content += "## 2. 💼 사업계획서 초안 (Business Plan Draft)\n\n"
        report_content += plan_result.answer + "\n\n"

        # 파일 저장
        report_file = "d:/yooyk1/notebooklm_mcp/MARKETING_REPORT.md"
        with open(report_file, "w", encoding="utf-8") as f:
            f.write(report_content)
            
        print(f"\n✅ 리포트 저장 완료: {report_file}", file=sys.stderr)
        
        # HTML 변환 및 태그 추가
        try:
            import markdown
            html = markdown.markdown(report_content, extensions=['tables', 'fenced_code'])
            html_path = report_file.replace(".md", ".html")
            
            style = """
            <style>
                body { 
                    font-family: 'Malgun Gothic', 'Noto Sans KR', sans-serif; 
                    max-width: 800px; 
                    margin: 0 auto; 
                    padding: 40px; 
                    line-height: 1.6; 
                    letter-spacing: -0.05em; 
                }
                h1, h2, h3 { color: #2c3e50; letter-spacing: -0.07em; }
                code { background: #eee; padding: 2px 5px; border-radius: 3px; }
                pre { background: #f4f4f4; padding: 15px; overflow-x: auto; }
                blockquote { border-left: 4px solid #3498db; padding-left: 15px; color: #555; }
            </style>
            """
            
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(f"<html><head><meta charset='utf-8'>{style}</head><body>{html}</body></html>")
                
            print(f"✅ HTML 변환 완료 (인쇄용): {html_path}", file=sys.stderr)
            
            import webbrowser
            webbrowser.open(f"file:///{html_path}")
            
        except ImportError:
            print("⚠️ markdown 모듈 없음, HTML 변환 생략", file=sys.stderr)

if __name__ == "__main__":
    asyncio.run(generate_marketing_content())
