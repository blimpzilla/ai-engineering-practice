from fastapi import FastAPI, HTTPException
from smart_copy import generate_copy, BRANDS, CONTENT_TYPES
from dotenv import load_dotenv
from openai import OpenAI
import os
from pydantic import BaseModel

app = FastAPI()

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY not found. Check your .env file in the repo root.")

client = OpenAI(api_key=api_key)

@app.get("/health")
def health():
    return {"status": "ok"}

class GenerateCopyRequest(BaseModel):
    brand_id: str
    content_type_id: str
    brief: str

@app.post("/generate-copy")
def generate_copy_endpoint(payload: GenerateCopyRequest):
    brand_id = payload.brand_id
    content_type_id = payload.content_type_id
    brief = payload.brief

    brand = next((b for b in BRANDS if b["id"] == brand_id), None)
    if brand is None:
        raise HTTPException(status_code=404, detail=f"Unknown brand_id: {brand_id}")

    content_type = next((ct for ct in CONTENT_TYPES if ct["id"] == content_type_id), None)
    if content_type is None:
        raise HTTPException(status_code=404, detail=f"Unknown content_type_id: {content_type_id}")

    try:
        result = generate_copy(client, brand, content_type, brief)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"options": result}
