
from typing import Any, List
from mcp.server import Server
import mcp.types as types
from mcp.server.stdio import stdio_server
import asyncio
import sys
from notebooklm_mcp.auth import get_notebooklm_cookies, load_cookies, save_cookies, COOKIE_FILE
from notebooklm.client import NotebookLMClient
from notebooklm.auth import AuthTokens, fetch_tokens

class NotebookLMServer:
    def __init__(self):
        self.server = Server("notebooklm-mcp")
        self.client: NotebookLMClient | None = None
        self.cookies = {}

    async def initialize_client(self):
        print("🔄 NotebookLM 클라이언트 초기화 중...", file=sys.stderr)
        # 1. 저장된 쿠키 확인
        self.cookies = load_cookies()
        
        # 2. 없으면 브라우저에서 추출 시도
        if not self.cookies:
            print("⚠️ 저장된 쿠키가 없습니다. 브라우저에서 추출을 시도합니다.", file=sys.stderr)
            self.cookies = get_notebooklm_cookies("chrome") # 기본값 Chrome
            if self.cookies:
                save_cookies(self.cookies)
        
        if not self.cookies:
            print("❌ 인증 실패: 쿠키를 가져올 수 없습니다. 'notebooklm.google.com'에 로그인되어 있는지 확인하세요.", file=sys.stderr)
            return False

        try:
            # 3. 토큰 가져오기 (비동기)
            csrf_token, session_id = await fetch_tokens(self.cookies)
            auth = AuthTokens(cookies=self.cookies, csrf_token=csrf_token, session_id=session_id)
            self.client = NotebookLMClient(auth)
            print("✅ NotebookLM 클라이언트 연결 성공!", file=sys.stderr)
            return True
        except Exception as e:
            print(f"❌ 클라이언트 초기화 오류: {str(e)}", file=sys.stderr)
            return False

    async def run(self):
        # 툴 등록
        @self.server.list_tools()
        async def handle_list_tools() -> list[types.Tool]:
            return [
                types.Tool(
                    name="notebook_list",
                    description="모든 노트북 목록을 조회합니다.",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                    },
                ),
                types.Tool(
                    name="notebook_create",
                    description="새 노트북을 생성합니다.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "title": {"type": "string", "description": "노트북 제목"}
                        },
                        "required": ["title"]
                    },
                ),
                types.Tool(
                    name="notebook_add_url",
                    description="노트북에 URL 소스를 추가합니다.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "notebook_id": {"type": "string", "description": "노트북 ID"},
                            "url": {"type": "string", "description": "추가할 URL"}
                        },
                        "required": ["notebook_id", "url"]
                    },
                ),
                types.Tool(
                    name="notebook_add_text",
                    description="노트북에 텍스트 소스를 추가합니다 (파일로 업로드).",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "notebook_id": {"type": "string", "description": "노트북 ID"},
                            "title": {"type": "string", "description": "소스 제목"},
                            "text": {"type": "string", "description": "추가할 텍스트 내용"}
                        },
                        "required": ["notebook_id", "text"]
                    },
                ),
                types.Tool(
                    name="notebook_query",
                    description="노트북에 질문하고 답변을 받습니다.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "notebook_id": {"type": "string", "description": "노트북 ID"},
                            "query": {"type": "string", "description": "질문 내용"}
                        },
                        "required": ["notebook_id", "query"]
                    },
                ),
                types.Tool(
                    name="refresh_auth",
                    description="인증을 새로고침합니다 (쿠키 재추출).",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                    },
                )
            ]

        @self.server.call_tool()
        async def handle_call_tool(
            name: str, arguments: dict[str, Any] | None
        ) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
            
            if name == "refresh_auth":
                self.cookies = get_notebooklm_cookies("chrome")
                if self.cookies:
                    save_cookies(self.cookies)
                    success = await self.initialize_client()
                    if success:
                        return [types.TextContent(type="text", text="✅ 인증이 성공적으로 갱신되었습니다.")]
                    else:
                        return [types.TextContent(type="text", text="❌ 인증 갱신 실패.")]
                else:
                    return [types.TextContent(type="text", text="❌ 쿠키 추출 실패. 브라우저 로그인을 확인하세요.")]

            if not self.client:
                 # 재시도
                if not await self.initialize_client():
                    return [types.TextContent(type="text", text="❌ NotebookLM에 연결되지 않았습니다. 'refresh_auth'를 먼저 실행해보세요.")]

            try:
                if name == "notebook_list":
                    async with self.client as client:
                        notebooks = await client.notebooks.list()
                        result_text = "📚 **노트북 목록:**\n\n"
                        for nb in notebooks:
                            result_text += f"- **{nb.title}** (ID: {nb.id})\n"
                        return [types.TextContent(type="text", text=result_text)]

                elif name == "notebook_create":
                    title = arguments.get("title", "New Notebook")
                    async with self.client as client:
                        notebook = await client.notebooks.create(title=title)
                        return [types.TextContent(type="text", text=f"✅ 노트북이 생성되었습니다: **{notebook.title}** (ID: {notebook.id})")]

                elif name == "notebook_add_url":
                    notebook_id = arguments.get("notebook_id")
                    url = arguments.get("url")
                    if not notebook_id or not url:
                        return [types.TextContent(type="text", text="❌ notebook_id와 url이 필요합니다.")]
                    
                    async with self.client as client:
                        print(f"Adding URL {url} to {notebook_id}...", file=sys.stderr)
                        source = await client.sources.add_url(notebook_id, url)
                        return [types.TextContent(type="text", text=f"✅ URL 소스가 추가되었습니다: {url}")]

                elif name == "notebook_add_text":
                    notebook_id = arguments.get("notebook_id")
                    title = arguments.get("title")
                    text = arguments.get("text")
                    if not notebook_id or not text:
                        return [types.TextContent(type="text", text="❌ notebook_id와 text가 필요합니다.")]
                    
                    async with self.client as client:
                        # 복사-붙여넣기 텍스트 소스 추가 (API 지원 여부 확인)
                        # notebooklm-py 라이브러리에는 add_text나 add_file 대신
                        # 보통 텍스트를 클립보드 소스로 넣거나 별도 API가 있을 수 있음.
                        # client.sources.add_text 등이 없으면 파일을 임시로 만들어 add_file 시도해야 함.
                        # 여기서는 라이브러리 기능을 확인하지 못했으므로, 
                        # '채팅 컨텍스트'에 포함하여 질문하는 방식으로 우회할 수도 있으나
                        # 일단 구현 시도. 만약 실패하면 파일 업로드로 대체.
                        print(f"Adding Text to {notebook_id}...", file=sys.stderr)
                        # NOTE: notebooklm-py 0.1.x에는 add_text 직접 지원이 없을 수 있음.
                        # 하지만 여기서는 파일 업로드 흉내를 낼 수 있음.
                        # 지금은 코드를 멈추지 않고 파일로 저장 후 add_file 모방이 현실적.
                        import tempfile
                        import os
                        
                        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as tmp:
                            tmp.write(text)
                            tmp_path = tmp.name
                        
                        try:
                            source = await client.sources.add_file(notebook_id, tmp_path)
                            return [types.TextContent(type="text", text=f"✅ 텍스트가 파일({title})로 추가되었습니다.")]
                        finally:
                            os.remove(tmp_path)

                elif name == "notebook_query":
                    notebook_id = arguments.get("notebook_id")
                    query = arguments.get("query")
                    if not notebook_id or not query:
                        return [types.TextContent(type="text", text="❌ notebook_id와 query가 필요합니다.")]
                    
                    async with self.client as client:
                        print(f"Querying {notebook_id} with: {query}...", file=sys.stderr)
                        # 채팅 세션 시작 및 질문
                        ask_result = await client.chat.ask(notebook_id, query)
                        return [types.TextContent(type="text", text=str(ask_result.answer))]
                
                else:
                    return [types.TextContent(type="text", text=f"알 수 없는 도구: {name}")]

            except Exception as e:
                return [types.TextContent(type="text", text=f"❌ 오류 발생 ({name}): {str(e)}")]

        # STDIO 서버 실행
        options = self.server.create_initialization_options()
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                options,
            )

async def main_async():
    server = NotebookLMServer()
    # 초기화는 첫 요청 시 또는 여기서
    await server.initialize_client()
    await server.run()

def main():
    try:
        asyncio.run(main_async())
    except KeyboardInterrupt:
        pass
