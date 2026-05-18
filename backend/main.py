import os
import base64
import uuid
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from services import analyze_and_generate_pattern
from pdf_generator import create_pattern_pdf

load_dotenv()

if not os.getenv("GEMINI_API_KEY"):
    raise RuntimeError("GEMINI_API_KEY environment variable is missing.")

app = FastAPI(title="Crochet Pattern Generator API")

# Configure CORS for React Frontend connectivity
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production environments
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure output directory for PDFs exists
PDF_OUTPUT_DIR = "static/patterns"
os.makedirs(PDF_OUTPUT_DIR, exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

class PatternRequest(BaseModel):
    item_type: str = Field(..., description="Type of item: scarf, beanie, granny square")
    yarn_size: str = Field(..., description="Size of yarn used")
    hook_size: str = Field(..., description="Size of crochet hook")
    image: str = Field(..., description="Base64 encoded string of the reference image")
    mode: str = Field("strict", description="Generation mode: strict or creative")

class PatternResponse(BaseModel):
    image_quality: str
    warning: str
    pdf_url: str
    raw_json: dict

@app.post("/generate-pattern", response_model=PatternResponse)
async def generate_pattern(payload: PatternRequest):
    try:
        # 1. Clean Base64 prefix string if present
        header_cutoff = payload.image.find(",")
        base64_data = payload.image[header_cutoff + 1:] if header_cutoff != -1 else payload.image
        
        image_bytes = base64.b64decode(base64_data)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid Base64 image encoding scheme.")

    # 2. Communicate with Gemini Engine
    gemini_output = await analyze_and_generate_pattern(
        image_bytes=image_bytes,
        item_type=payload.item_type,
        yarn_size=payload.yarn_size,
        hook_size=payload.hook_size,
        mode=payload.mode
    )
    
    # 3. Generate Downloadable Document
    filename = f"pattern_{uuid.uuid4().hex}.pdf"
    pdf_path = os.path.join(PDF_OUTPUT_DIR, filename)
    
    success = create_pattern_pdf(
        file_path=pdf_path,
        data=gemini_output,
        meta={
            "item_type": payload.item_type,
            "yarn_size": payload.yarn_size,
            "hook_size": payload.hook_size
        }
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Failed compiling PDF documentation file asset."
        )

    # Resolve application absolute routing link
    pdf_url = f"http://localhost:8000/static/patterns/{filename}"

    return PatternResponse(
        image_quality=gemini_output.get("image_quality", "low"),
        warning=gemini_output.get("warning", ""),
        pdf_url=pdf_url,
        raw_json=gemini_output
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", 8000)), reload=True)