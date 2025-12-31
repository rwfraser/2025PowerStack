from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agent import agent
from langchain_core.messages import HumanMessage
from typing import Optional
import uuid

app = FastAPI(title="AI Agent API 2025 with Memory")

class ChatRequest(BaseModel):
    message: str
    thread_id: Optional[str] = None  # Optional conversation thread ID

class ChatResponse(BaseModel):
    response: str
    thread_id: str

class HistoryRequest(BaseModel):
    thread_id: str

@app.get("/")
def root():
    return {
        "message": "AI Agent API with Memory is running. Visit /docs for API documentation.",
        "features": ["Persistent conversation memory", "Thread-based conversations"]
    }

@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    """
    Chat with the AI agent. Provide a thread_id to continue a conversation,
    or omit it to start a new conversation.
    """
    # Generate or use provided thread_id
    thread_id = request.thread_id or str(uuid.uuid4())
    
    # Initialize the state with the user message
    inputs = {"messages": [HumanMessage(content=request.message)]}
    
    # Configuration for the agent with thread ID for memory persistence
    config = {"configurable": {"thread_id": thread_id}}
    
    try:
        # Run the agent with memory (synchronous)
        result = agent.invoke(inputs, config=config)
        
        # Return the last message from the AI along with thread_id
        return ChatResponse(
            response=result["messages"][-1].content,
            thread_id=thread_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent error: {str(e)}")

@app.post("/history")
def get_conversation_history(request: HistoryRequest):
    """
    Retrieve the conversation history for a given thread_id.
    """
    config = {"configurable": {"thread_id": request.thread_id}}
    
    try:
        # Get the current state for this thread
        state = agent.get_state(config)
        
        if not state or not state.values.get("messages"):
            return {"thread_id": request.thread_id, "messages": [], "message": "No history found"}
        
        # Format messages for response
        messages = []
        for msg in state.values["messages"]:
            messages.append({
                "type": msg.__class__.__name__,
                "content": msg.content,
            })
        
        return {
            "thread_id": request.thread_id,
            "messages": messages
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving history: {str(e)}")

@app.post("/new-conversation")
def new_conversation():
    """
    Generate a new conversation thread ID.
    """
    thread_id = str(uuid.uuid4())
    return {"thread_id": thread_id, "message": "New conversation started"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)