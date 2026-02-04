
import markdown
import sys
import os
from datetime import datetime

REPORT_FILE = "d:/yooyk1/notebooklm_mcp/MARKETING_REPORT.md"
HTML_FILE = "d:/yooyk1/notebooklm_mcp/MARKETING_REPORT.html"

def update_report(title, content):
    # MD 파일에 추가
    with open(REPORT_FILE, "a", encoding="utf-8") as f:
        f.write(f"\n\n---\n\n## {title}\n\n")
        f.write(content + "\n")
    
    print(f"✅ 리포트에 '{title}' 섹션 추가 완료", file=sys.stderr)

    # HTML 재생성
    with open(REPORT_FILE, "r", encoding="utf-8") as f:
        full_text = f.read()
        
    html_content = markdown.markdown(full_text, extensions=['tables', 'fenced_code'])
    
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
        table { border-collapse: collapse; width: 100%; margin: 20px 0; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
    </style>
    """
    
    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(f"<html><head><meta charset='utf-8'>{style}</head><body>{html_content}</body></html>")
        
    print(f"✅ HTML 업데이트 완료: {HTML_FILE}", file=sys.stderr)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python update_report.py <title> <content_file>", file=sys.stderr)
        sys.exit(1)
        
    title_arg = sys.argv[1]
    content_file_arg = sys.argv[2]
    
    with open(content_file_arg, "r", encoding="utf-8") as f:
        content_arg = f.read()
        
    update_report(title_arg, content_arg)
