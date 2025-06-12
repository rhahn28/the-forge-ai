# core/file_client.py
import httpx

class FileSystemClient:
    """
    This is the agent's 'remote control' for the FileSystemMCPServer.
    It's a dedicated client that knows how to format requests and talk to our tool.
    By putting it in its own file, any agent can import and use it without conflicts.
    """
    def __init__(self, base_url="http://127.0.0.1:8000"):
        self.base_url = base_url

    async def list_files(self, path="."):
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{self.base_url}/list_files", json={"path": path})
            response.raise_for_status()
            return response.json().get('files', [])

    async def write_file(self, path: str, content: str):
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{self.base_url}/write_file", json={"path": path, "content": content})
            response.raise_for_status()
            return response.json()
        
    async def read_file(self, path: str):
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{self.base_url}/read_file", json={"path": path})
            response.raise_for_status()
            return response.json()['content']