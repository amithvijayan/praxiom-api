from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional, Any
import uvicorn
import uuid

from database import get_db, engine as db_engine, Base
from models import ChatSession, ChatMessage

app = FastAPI(
    title="Praxiom Multi-Agent Swarm (Core v2.0)",
    version="0.2.0"
)

# Allow CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    # Create tables if they don't exist (useful for local SQLite dev)
    async with db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

class ChatPayload(BaseModel):
    session_id: str
    message: str

from engine.registry import EngineRegistry
import engine.engineering.bess_sizing
import engine.engineering.transformer_sizing
import engine.engineering.load_flow_analysis
import engine.sustainability.ghg_protocol
import engine.sustainability.carbon_tax_liability
import engine.sustainability.decarbonization_roi
import engine.utility_business.financials
import engine.utility_business.ppa_modeling
import engine.utility_business.policy_compliance
import engine.memory.autonomous_crawler
from engine.memory.vector_memory import VectorMemoryVault

import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# Initialize the Gemini Model with our Universal Engine tools
system_instruction = (
    "You are Praxiom Core v3.0, an expert Orchestrator for ISTA. "
    "Your job is to extract parameters from user prompts and call your registered Physics Engines and Tools. "
    "If the user provides a URL or asks you to read a webpage, use the web_crawler tool. "
    "You MUST NEVER perform mathematical calculations yourself. Always call a tool. "
    "If no tool matches, use the Context provided to answer the question without hallucinating."
)
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash", 
    system_instruction=system_instruction,
    tools=EngineRegistry.get_gemini_tools()
)

@app.post("/api/v1/chat/stream")
async def route_chat_query(payload: ChatPayload, db: AsyncSession = Depends(get_db)):
    """
    Route Chat Query: Intercepts prompt, retrieves RAG context, uses Gemini to trigger tools.
    """
    # 1. Ensure the session exists
    result = await db.execute(select(ChatSession).where(ChatSession.id == payload.session_id))
    session = result.scalars().first()
    if not session:
        new_session = ChatSession(id=payload.session_id, title="Multi-Agent Terminal")
        db.add(new_session)
        await db.commit()

    # 2. Save user message
    user_msg = ChatMessage(
        id=str(uuid.uuid4()),
        session_id=payload.session_id,
        role="user",
        text=payload.message
    )
    db.add(user_msg)

    bot_response = "Praxiom encountered an error."
    tools_used = []
    chart_data = None

    try:
        # 3. RAG: Retrieve context from Pinecone Permanent Memory
        try:
            import asyncio
            vault = VectorMemoryVault.get_instance()
            context = await asyncio.to_thread(vault.recall_facts, payload.message)
        except Exception as memory_err:
            context = f"(Pinecone Memory Offline: {str(memory_err)})"

        # Formulate Augmented Prompt
        prompt = payload.message
        if context and "Offline" not in context:
            prompt = f"{context}\n\nUser Prompt: {payload.message}"

        # Call Gemini asynchronously
        response = await model.generate_content_async(prompt)

        
        # Check if Gemini decided to call one of our tools
        if response.parts and getattr(response.parts[0], 'function_call', None):
            fc = response.parts[0].function_call
            function_name = fc.name
            args = dict(fc.args)
            
            # Since auto-execution is tricky with **kwargs, we'll manually route it 
            # to our registry using the function name it predicted.
            engine_name = function_name.replace("execute_", "")
            
            # Log the tool usage
            tools_used.append(function_name)
            
            # Execute the strict deterministic engine without blocking the async event loop
            import asyncio
            engine_res = await asyncio.to_thread(EngineRegistry.execute, engine_name, args)
            
            bot_response = engine_res["result_text"]
            chart_data = engine_res["chart_data"]
            
        else:
            # Gemini decided not to call a tool, so we just return its plain text answer.
            bot_response = response.text
            
    except Exception as e:
        bot_response = f"Agentic Orchestrator Error: {str(e)}"

    # 4. Save bot message
    bot_msg = ChatMessage(
        id=str(uuid.uuid4()),
        session_id=payload.session_id,
        role="assistant",
        text=bot_response,
        tools_used=tools_used,
        chart_data=chart_data
    )
    db.add(bot_msg)
    await db.commit()

    # Mocking the response format expected by Next.js
    return {
        "result": bot_response,
        "tools": tools_used,
        "chartData": chart_data
    }

@app.get("/api/v1/chat/history")
async def get_chat_history(session_id: str, db: AsyncSession = Depends(get_db)):
    """
    Fetch Chat History for the Memory Vaults.
    """
    result = await db.execute(
        select(ChatMessage)
        .where(ChatMessage.session_id == session_id)
        .order_by(ChatMessage.created_at.asc())
    )
    messages = result.scalars().all()
    
    return [
        {
            "id": msg.id,
            "role": msg.role,
            "text": msg.text,
            "toolsUsed": msg.tools_used,
            "chartData": msg.chart_data
        } for msg in messages
    ]

@app.get("/")
def read_root():
    return {"status": "Praxiom Core v2.0 Online"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
