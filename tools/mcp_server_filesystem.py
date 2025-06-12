# tools/mcp_server_filesystem.py

from fastapi import FastAPI
from pydantic import BaseModel
import os

app = FastAPI()

class FilePayload(BaseModel):
    path: str
    content: str

@app.post("/write_file")
async def write_file(payload: FilePayload):
    parent_dir = os.path.dirname(payload.path)
    if parent_dir and not os.path.exists(parent_dir):
        os.makedirs(parent_dir, exist_ok=True)

    with open(payload.path, "w", encoding="utf-8") as f:
        f.write(payload.content)

    print(f"[FILE SERVER] Wrote file: {payload.path}")
    return {"status": "success"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
