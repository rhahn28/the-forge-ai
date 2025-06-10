# tools/mcp_server_filesystem.py

import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

# <<< MAKE SURE THIS LINE EXISTS AND IS SPELLED CORRECTLY
app = FastAPI()

class FilePayload(BaseModel):
    path: str
    content: str | None = None

@app.post("/write_file")
async def write_file(payload: FilePayload):
    try:
        safe_path = os.path.join('.', os.path.basename(payload.path))
        
        with open(safe_path, 'w', encoding='utf-8') as f:
            f.write(payload.content)
            
        print(f"INFO: Successfully wrote to file '{safe_path}'")
        return {"status": "success", "message": f"File '{safe_path}' written."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/read_file")
async def read_file(payload: FilePayload):
    try:
        safe_path = os.path.join('.', os.path.basename(payload.path))
        
        with open(safe_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        print(f"INFO: Successfully read from file '{safe_path}'")
        return {"status": "success", "content": content}
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"File not found or could not be read: {e}")

if __name__ == "__main__":
    print("Starting File System MCP Server on http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)