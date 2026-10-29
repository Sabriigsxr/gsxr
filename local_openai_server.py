#!/usr/bin/env python3
"""
Local OpenAI-compatible API Server for Qwen2.5-Coder-3B
Serves the local model directly via OpenAI-compatible API with API Key auth.
"""

import os
import httpx
from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from typing import Optional, List, Dict, Any, AsyncGenerator
from typing_extensions import Self
import logging
from contextlib import asynccontextmanager

# Configuration
LOCAL_BASE_URL = "http://127.0.0.1:11434"  # Ollama root (OpenAI-compatible /v1 lives under it)
MODEL_NAME = "pentest-bughunter:latest"  # model served by local Ollama
API_KEY = os.getenv("LOCAL_API_KEY", "sk-local-12345")  # Set your API key here

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# API Key authentication
api_key_header = APIKeyHeader(name="Authorization", auto_error=False)

async def verify_api_key(authorization: str = Security(api_key_header)):
    """Verify the API key from Authorization header."""
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    
    # Support both "Bearer sk-xxx" and "sk-xxx" formats
    api_key = authorization.replace("Bearer ", "") if authorization.startswith("Bearer ") else authorization
    
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    return api_key

local_client: httpx.AsyncClient = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global local_client
    local_client = httpx.AsyncClient(base_url=LOCAL_BASE_URL, timeout=300.0)
    logger.info(f"Local OpenAI Server started, proxying to {LOCAL_BASE_URL}")
    yield
    await local_client.aclose()
    logger.info("Local OpenAI Server stopped")


app = FastAPI(
    title="Local Qwen2.5-Coder OpenAI API",
    description="OpenAI-compatible API for local Qwen2.5-Coder-3B",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# OpenAI-compatible models
class Message(BaseModel):
    role: str
    content: str
    name: Optional[str] = None


class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[Dict[str, str]]
    max_tokens: Optional[int] = None
    temperature: Optional[float] = 0.7
    top_p: Optional[float] = 1.0
    stream: Optional[bool] = False
    stop: Optional[List[str]] = None
    presence_penalty: Optional[float] = 0.0
    frequency_penalty: Optional[float] = 0.0
    logit_bias: Optional[Dict[str, float]] = None
    user: Optional[str] = None


class CompletionRequest(BaseModel):
    model: str
    prompt: str
    max_tokens: Optional[int] = None
    temperature: Optional[float] = 0.7
    top_p: Optional[float] = 1.0
    stream: Optional[bool] = False
    stop: Optional[List[str]] = None
    presence_penalty: Optional[float] = 0.0
    frequency_penalty: Optional[float] = 0.0
    logit_bias: Optional[Dict[str, float]] = None
    user: Optional[str] = None
    echo: Optional[bool] = False


class Model(BaseModel):
    id: str
    object: str = "model"
    created: int
    owned_by: str


class ModelList(BaseModel):
    object: str = "list"
    data: List[Dict[str, Any]]


@app.get("/health")
async def health():
    try:
        # Ollama exposes /api/version as a liveness probe (no /v1/health endpoint).
        async with httpx.AsyncClient(timeout=5.0) as client:
            r = await client.get("http://127.0.0.1:11434/api/version")
        return {"status": "healthy" if r.status_code == 200 else "unhealthy"}
    except Exception:
        return {"status": "unhealthy"}


@app.get("/v1/models")
async def list_models(api_key: str = Depends(verify_api_key)):
    try:
        r = await local_client.get("/models", timeout=10.0)
        if r.status_code == 200:
            return r.json()
    except Exception as e:
        logger.warning(f"Failed to fetch models: {e}")
    
    return {
        "object": "list",
        "data": [
            {
                "id": MODEL_NAME,
                "object": "model",
                "created": 1700000000,
                "owned_by": "local"
            }
        ]
    }


@app.post("/v1/chat/completions")
async def chat_completions(request: ChatCompletionRequest, api_key: str = Depends(verify_api_key)):
    """Chat completions - routes to local llama.cpp server."""
    # The local server supports chat completions
    req_data = request.model_dump(exclude_none=True)
    req_data["model"] = MODEL_NAME
    
    try:
        if request.stream:
            async def stream():
                async with local_client.stream("POST", "/chat/completions", json=req_data, timeout=300.0) as resp:
                    if resp.status_code != 200:
                        error = await resp.aread()
                        raise HTTPException(status_code=resp.status_code, detail=error.decode())
                    async for chunk in resp.aiter_bytes():
                        yield chunk
            
            return StreamingResponse(
                stream(),
                media_type="text/event-stream",
                headers={"Cache-Control": "no-cache", "Connection": "keep-alive"}
            )
        else:
            resp = await local_client.post("/chat/completions", json=req_data, timeout=300.0)
            if resp.status_code != 200:
                raise HTTPException(status_code=resp.status_code, detail=resp.text)
            return JSONResponse(content=resp.json())
    
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Backend timeout")
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=f"Backend unavailable: {str(e)}")


@app.post("/v1/completions")
async def completions(request: CompletionRequest, api_key: str = Depends(verify_api_key)):
    """Text completions."""
    req_data = request.model_dump(exclude_none=True)
    req_data["model"] = MODEL_NAME
    
    try:
        if request.stream:
            async def stream():
                async with local_client.stream("POST", "/completions", json=req_data, timeout=300.0) as resp:
                    if resp.status_code != 200:
                        error = await resp.aread()
                        raise HTTPException(status_code=resp.status_code, detail=error.decode())
                    async for chunk in resp.aiter_bytes():
                        yield chunk
            
            return StreamingResponse(
                stream(),
                media_type="text/event-stream",
                headers={"Cache-Control": "no-cache", "Connection": "keep-alive"}
            )
        else:
            resp = await local_client.post("/completions", json=req_data, timeout=300.0)
            if resp.status_code != 200:
                raise HTTPException(status_code=resp.status_code, detail=resp.text)
            return JSONResponse(content=resp.json())
    
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Backend timeout")
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=f"Backend unavailable: {str(e)}")


@app.get("/v1/models/{model_id}")
async def get_model(model_id: str):
    if model_id != MODEL_NAME:
        raise HTTPException(status_code=404, detail="Model not found")
    return {
        "id": MODEL_NAME,
        "object": "model",
        "created": 1700000000,
        "owned_by": "local"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)