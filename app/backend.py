import logging
import os
import sys
from typing import Optional

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.chat_engine import get_engine
from src.config import LOG_LEVEL, LOG_FORMAT

# ---------- App and Logging Setup ----------
# Configure logging
logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="CS3249 Assignment 1 Backend",
    description="Backend API for the Conversational User Interface",
    version="0.1.0",
)


# ---------- Data Models ----------
class ChatRequest(BaseModel):
    """Request model for the /chat endpoint."""

    message: str


# ---------- API Endpoints ----------
@app.post("/chat")
async def handle_chat(request: ChatRequest):
    """
    Handle a single chat message from the user.
    """
    try:
        engine = get_engine()
        result = engine.process_message(request.message)
        return result
    except Exception as e:
        logger.error(f"Error processing chat request: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post("/reset")
async def reset_engine():
    """
    Reset the chat engine.
    """
    try:
        engine = get_engine()
        engine.reset()
        return {"message": "Engine reset"}
    except Exception as e:
        logger.error(f"Error resetting engine: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")


# ---------- Main Entry Point ----------
if __name__ == "__main__":
    import uvicorn

    logger.info("Starting backend server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
