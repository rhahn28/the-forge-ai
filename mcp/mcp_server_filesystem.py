# mcp/mcp_server_filesystem.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional # <<< NEW IMPORT
import os

app = FastAPI()

class FilePayload(BaseModel):
    path: str
    content: Optional[str] = None # <<< THE FIX: Content is now optional.

@app.post("/write_file")
async def write_file(payload: FilePayload):
    # Ensure parent directory exists
    parent_dir = os.path.dirname(payload.path)
    if parent_dir and not os.path.exists(parent_dir):
        os.makedirs(parent_dir, exist_ok=True)

    # Use the provided content, or an empty string if it's None.
    content_to_write = payload.content if payload.content is not None else ""
    
    with open(payload.path, "w", encoding="utf-8") as f:
        f.write(content_to_write)

    print(f"[FILE SERVER] Wrote to file: {payload.path}")
    return {"status": "success"}

# Add back the list_files endpoint, as the Planner uses it
@app.post("/list_files")
async def list_files(payload: BaseModel): # Does not need a specific payload
    try:
        files = os.listdir(".")
        return {"status": "success", "files": files}
    except Exception as e:
        return {"status": "error", "detail": str(e)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)