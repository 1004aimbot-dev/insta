
import markdown
import os
import webbrowser

MD_FILE = "d:/yooyk1/notebooklm_mcp/YANGPYEONG_BUSINESS_PLAN.md"
HTML_FILE = "d:/yooyk1/notebooklm_mcp/YANGPYEONG_BUSINESS_PLAN.html"

CSS_STYLE = """
<style>
    body { font-family: 'Malgun Gothic', sans-serif; line-height: 1.6; max-width: 800px; margin: 0 auto; padding: 40px; }
    h1 { color: #2c3e50; border-bottom: 2px solid #2c3e50; padding-bottom: 10px; }
    h2 { color: #34495e; margin-top: 30px; border-bottom: 1px solid #eee; padding-bottom: 5px; }
    h3 { color: #16a085; }
    code { background-color: #f8f9fa; padding: 2px 5px; border-radius: 3px; }
    pre { background-color: #f8f9fa; padding: 15px; border-radius: 5px; overflow-x: auto; }
    blockquote { border-left: 5px solid #bdc3c7; margin: 0; padding-left: 15px; color: #7f8c8d; }
    table { border-collapse: collapse; width: 100%; margin: 20px 0; }
    th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
    th { background-color: #f2f2f2; }
    @media print {
        body { padding: 0; }
        a { text-decoration: none; color: black; }
    }
</style>
"""

def convert_and_open():
    try:
        with open(MD_FILE, 'r', encoding='utf-8') as f:
            text = f.read()
            
        html_content = markdown.markdown(text, extensions=['tables', 'fenced_code'])
        
        full_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>양평 사업계획서</title>
            {CSS_STYLE}
        </head>
        <body>
            {html_content}
            <script>
                // 자동 인쇄 대화상자 띄우기 (선택사항)
                // window.print(); 
            </script>
        </body>
        </html>
        """
        
        with open(HTML_FILE, 'w', encoding='utf-8') as f:
            f.write(full_html)
            
        print(f"✅ HTML 변환 완료: {HTML_FILE}")
        print("🌍 브라우저에서 엽니다...")
        webbrowser.open(f"file:///{HTML_FILE}")
        
    except Exception as e:
        print(f"❌ 변환 실패: {e}")
        # markdown 패키지가 없을 경우 안내
        print("💡 'pip install markdown' 명령어로 라이브러리 설치가 필요할 수 있습니다.")

if __name__ == "__main__":
    convert_and_open()
