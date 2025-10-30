from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

# Add CORS middleware - allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class AttachmentRequest(BaseModel):
    attachments: Dict[str, str]

class MimeTypeResponse(BaseModel):
    type: str

def detect_mime_category(data_uri: str) -> str:
    """Extract and categorize MIME type from data URI."""
    try:
        if not data_uri.startswith("data:"):
            return "unknown"
        
        mime_part = data_uri.split(";")[0].replace("data:", "")
        
        if "/" in mime_part:
            category = mime_part.split("/")[0]
            
            if category in ["image", "text", "application"]:
                return category
            else:
                return "unknown"
        
        return "unknown"
    except Exception:
        return "unknown"

@app.post("/file", response_model=MimeTypeResponse)
async def detect_file_type(request: AttachmentRequest):
    """Detect MIME type from data URI."""
    data_uri = request.attachments.get("url", "")
    mime_type = detect_mime_category(data_uri)
    return {"type": mime_type}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
