# core/file_client.py
import httpx

class FileSystemClient:
    def __init__(self, base_url="http://127.0.0.1:8000"):
        self.base_url = base_url

    async def write_file(self, path: str, content: str):
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{self.base_url}/write_file", json={"path": path, "content": content})
            response.raise_for_status()
            return response.json()