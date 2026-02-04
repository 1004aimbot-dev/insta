
from notebooklm_mcp.auth import get_notebooklm_cookies
import sys

def test_auth():
    print("🧪 인증 테스트 시작...")
    cookies = get_notebooklm_cookies("chrome")
    if cookies:
        print("\n✨ 쿠키 추출 성공!")
        print(f"🔑 추출된 쿠키 개수: {len(cookies)}")
        # 보안상 쿠키 값 전체는 출력하지 않음
        print("✅ 인증 모듈이 정상 작동합니다.")
    else:
        print("\n❌ 쿠키 추출 실패.")
        print("👉 Chrome 브라우저에서 NotebookLM(notebooklm.google.com)에 로그인되어 있는지 확인하세요.")

if __name__ == "__main__":
    test_auth()
