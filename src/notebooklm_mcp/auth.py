
import browser_cookie3
import os
import json
import sys
import shutil
import tempfile
import glob
from typing import Dict, Optional

COOKIE_FILE = "auth_cookies.json"

def get_notebooklm_cookies(browser_name: str = "chrome") -> Dict[str, str]:
    """
    브라우저에서 NotebookLM 쿠키를 추출합니다.
    DB 잠금(Lock) 발생 시 임시 파일로 복사하여 시도합니다.
    """
    print(f"🔄 {browser_name} 브라우저에서 쿠키 추출 중...", file=sys.stderr)
    
    cj = None
    try:
        # 1차 시도: 표준 방식
        if browser_name.lower() == "chrome":
            cj = browser_cookie3.chrome(domain_name="notebooklm.google.com")
        elif browser_name.lower() == "firefox":
            cj = browser_cookie3.firefox(domain_name="notebooklm.google.com")
        elif browser_name.lower() == "edge":
            cj = browser_cookie3.edge(domain_name="notebooklm.google.com")
        else:
            cj = browser_cookie3.load(domain_name="notebooklm.google.com")
            
    except Exception as e:
        if "database is locked" in str(e) and browser_name.lower() == "chrome":
            print(f"⚠️ 브라우저 DB가 잠겨있습니다. 우회 시도 중...", file=sys.stderr)
            try:
                # Windows Chrome Cookie 경로 찾기
                local_app_data = os.environ.get("LOCALAPPDATA", "")
                cookie_path_pattern = os.path.join(local_app_data, r"Google\Chrome\User Data\Default\Network\Cookies")
                
                # Default 프로필이 아닐 수도 있으므로 패턴 매칭 시도 가능하지만, 일단 Default 우선
                if not os.path.exists(cookie_path_pattern):
                     # Network 폴더가 없는 구버전이나 다른 프로필일 수 있음
                     cookie_path_pattern = os.path.join(local_app_data, r"Google\Chrome\User Data\*\Network\Cookies")
                     matches = glob.glob(cookie_path_pattern)
                     if matches:
                         cookie_path_pattern = matches[0]
                
                if os.path.exists(cookie_path_pattern):
                    # 임시 파일로 복사
                    tmp_dir = tempfile.gettempdir()
                    tmp_cookie_file = os.path.join(tmp_dir, "notebooklm_cookies_tmp")
                    shutil.copy2(cookie_path_pattern, tmp_cookie_file)
                    
                    print(f"📋 쿠키 파일을 임시 경로로 복사했습니다: {tmp_cookie_file}", file=sys.stderr)
                    cj = browser_cookie3.chrome(cookie_file=tmp_cookie_file, domain_name="notebooklm.google.com")
                else:
                    print(f"❌ Chrome 쿠키 파일을 찾을 수 없습니다: {cookie_path_pattern}", file=sys.stderr)
                    raise e
            except Exception as e2:
                print(f"❌ 우회 시도 실패: {str(e2)}", file=sys.stderr)
                # 원본 에러 출력
                print(f"❌ 원본 추출 실패: {str(e)}", file=sys.stderr)
                return {}
        else:
            print(f"❌ 쿠키 추출 실패: {str(e)}", file=sys.stderr)
            return {}

    if not cj:
        return {}
        
    cookies = {c.name: c.value for c in cj}
    if not cookies:
        print("❌ 쿠키를 찾을 수 없습니다. NotebookLM에 로그인되어 있는지 확인해주세요.", file=sys.stderr)
        return {}
        
    print(f"✅ {len(cookies)}개의 쿠키를 성공적으로 추출했습니다.", file=sys.stderr)
    return cookies

def save_cookies(cookies: Dict[str, str], filepath: str = COOKIE_FILE):
    """쿠키를 파일로 저장합니다."""
    try:
        with open(filepath, 'w') as f:
            json.dump(cookies, f)
        print(f"💾 쿠키가 {filepath}에 저장되었습니다.", file=sys.stderr)
    except Exception as e:
        print(f"❌ 쿠키 저장 실패: {str(e)}", file=sys.stderr)

def load_cookies(filepath: str = COOKIE_FILE) -> Optional[Dict[str, str]]:
    """파일에서 쿠키를 불러옵니다."""
    if not os.path.exists(filepath):
        return None
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ 쿠키 로드 실패: {str(e)}", file=sys.stderr)
        return None
