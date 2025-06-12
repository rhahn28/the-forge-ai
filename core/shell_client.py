# core/shell_client.py
import httpx

class ShellClient:
    def __init__(self, base_url="http://127.0.0.1:8001"):
        self.base_url = base_url

    async def run_command(self, command: str):
        async with httpx.AsyncClient(timeout=30.0) as client:
            # This ensures the client is also calling "/run_shell"
            url_path = "/run_shell"
            print(f"SHELL_CLIENT: Sending command '{command}' to {self.base_url}{url_path}")
            response = await client.post(f"{self.base_url}{url_path}", json={"command": command})
            response.raise_for_status()
            return response.json()