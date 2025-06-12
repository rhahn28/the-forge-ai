# tools/mcp_server_filesystem.py
import os
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class FilePayload(BaseModel):
    path: str
    content: str | None = None

@app.post("/list_files")
async def list_files(payload: FilePayload):
    """Lists files in the current directory."""
    try:
        path = "." # For security, only allow listing the current project directory.
        files = os.listdir(path)
        print(f"INFO (File Server): Successfully listed files.")
        return {"status": "success", "files": files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/write_file")
async def write_file(payload: FilePayload):
    """Creates or overwrites a file with new content."""
    try:
        # Security measure to prevent writing files outside the project directory.
        safe_path = os.path.join('.', os.path.basename(payload.path))
        
        # Ensure parent directory exists for nested paths like tests/test.py
        if os.path.dirname(safe_path):
            os.makedirs(os.path.dirname(safe_path), exist_ok=True)

        with open(safe_path, 'w', encoding='utf-8') as f:
            f.write(payload.content)
            
        print(f"INFO (File Server): Successfully wrote to file '{safe_path}'")
        return {"status": "success", "message": f"File '{safe_path}' written."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/read_file")
async def read_file(payload: FilePayload):
    """Reads the content of a file."""
    try:
        safe_path = os.path.join('.', os.path.basename(payload.path))
        with open(safe_path, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"INFO (File Server): Successfully read from file '{safe_path}'")
        return {"status": "success", "content": content}
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"File not found or could not be read: {e}")

if __name__ == "__main__":
    # This server runs on port 8000
    print("Starting File System MCP Server on http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)