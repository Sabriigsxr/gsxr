#!/usr/bin/env bash
# =============================================================================
# GSXR Local Infrastructure Startup Script
# Starts: Ollama, OpenAI API Server, CPP Proxy/CLIProxyAPI, HexStrike Backend, RAG MCP
# =============================================================================
set -euo pipefail

export OLLAMA_NUM_GPU=0
export CUDA_VISIBLE_DEVICES=""
export OLLAMA_HOST=127.0.0.1:11434
export OLLAMA_KEEP_ALIVE=10m
export LOCAL_API_KEY=sk-local-12345
export TMPDIR=/home/gsxr/tmp
export RAG_DB=/home/gsxr/tmp

mkdir -p /home/gsxr/tmp /home/gsxr/oauth

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"; }

# --- 1. Ollama ---
log "Starting Ollama on 127.0.0.1:11434..."
pkill -f '^ollama serve$' 2>/dev/null || true
sleep 2
nohup ollama serve >> /home/gsxr/tmp/ollama_serve.log 2>&1 &
sleep 4
if curl -sm 5 -o /dev/null http://127.0.0.1:11434/api_tags 2>/dev/null || curl -sm 5 -o /dev/null http://127.0.0.1:11434/api/tags 2>/dev/null; then
    log "Ollama UP"
else
    log "WARNING: Ollama may not be ready yet"
fi

# --- 2. OpenAI API Server (port 8001) ---
log "Starting Local OpenAI API Server on port 8001..."
pkill -f 'local_openai_server.py' 2>/dev/null || true
sleep 1
nohup python3 /home/gsxr/local_openai_server.py >> /home/gsxr/tmp/openai_server.log 2>&1 &
sleep 3
if curl -sm 5 -o /dev/null -H "Authorization: Bearer sk-local-12345" http://127.0.0.1:8001/v1/models 2>/dev/null; then
    log "OpenAI API Server UP on port 8001"
else
    log "WARNING: OpenAI API Server may not be ready yet"
fi

# --- 3. CPP Proxy / CLIProxyAPI (port 8317) ---
log "Starting CLIProxyAPI (CPP Proxy) on port 8317..."
pkill -f 'cli-proxy-api' 2>/dev/null || true
sleep 1
cd /home/gsxr/bin/cpa-core
nohup /home/gsxr/bin/cpa-core/cli-proxy-api -config /home/gsxr/bin/cpa-core/config.yaml >> /home/gsxr/tmp/cpp_proxy.log 2>&1 &
sleep 3
if curl -sm 5 -o /dev/null http://127.0.0.1:8317/ 2>/dev/null; then
    log "CPP Proxy UP on port 8317"
else
    log "WARNING: CPP Proxy may not be ready yet"
fi

# --- 4. HexStrike Backend (port 8888) ---
log "Starting HexStrike Backend on port 8888..."
pkill -f 'hexstrike_server.py' 2>/dev/null || true
sleep 1
nohup python3 /usr/share/hexstrike-ai/hexstrike_server.py >> /home/gsxr/tmp/hexstrike_server.log 2>&1 &
sleep 5
if curl -sm 5 -o /dev/null http://127.0.0.1:8888/ 2>/dev/null; then
    log "HexStrike Backend UP on port 8888"
else
    log "WARNING: HexStrike Backend may not be ready yet"
fi

# --- 5. RAG MCP Server ---
log "RAG MCP Server (PID already running or started by OpenCode)..."
if ! pgrep -f 'rag_mcp.py' > /dev/null 2>&1; then
    nohup python3 /home/gsxr/rag_mcp.py >> /home/gsxr/tmp/rag_mcp.log 2>&1 &
    log "RAG MCP Server started"
else
    log "RAG MCP Server already running"
fi

log "=========================================="
log "All local infrastructure services started."
log "Ollama:        http://127.0.0.1:11434"
log "OpenAI API:    http://127.0.0.1:8001/v1"
log "CPP Proxy:     http://127.0.0.1:8317/"
log "HexStrike:     http://127.0.0.1:8888/"
log "=========================================="