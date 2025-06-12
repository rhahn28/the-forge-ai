# core/shell_client.py

import httpx

class ShellClient:
    def __init__(self, base_url="http://127.0.0.1:8001"):  # 🔧 Use your correct port here
        self.base_url = base_url

    async def run_command(self, command: str, venv_path: str = None, extra_env: dict = None):
        async with httpx.AsyncClient(timeout=30.0) as client:
            url_path = "/run_shell"
            payload = {
                "command": command,
                "venv_path": venv_path,
                "extra_env": extra_env
            }
            print(f"SHELL_CLIENT: Sending command '{command}' with venv '{venv_path}' to {self.base_url}{url_path}")

            try:
                response = await client.post(f"{self.base_url}{url_path}", json=payload)
                response.raise_for_status()
                return response.json()

            except httpx.HTTPStatusError as e:
                print(f"🔥 HTTPStatusError: {e.response.status_code} - {e.response.text}")
                return {'error': f'HTTPError {e.response.status_code}: {e.response.text}'}

            except httpx.RequestError as e:
                print(f"🔥 RequestError: {str(e)}")
                return {'error': f'ConnectionError: {str(e)}'}

            except Exception as e:
                print(f"🔥 Unexpected exception: {str(e)}")
                return {'error': f'UnhandledError: {str(e)}'}
