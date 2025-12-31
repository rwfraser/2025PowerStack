from fastapi import FastAPI
from pydantic import BaseModel
from agent import agent
from langchain_core.messages import HumanMessage

app = FastAPI(title="AI Agent API 2025")

class ChatRequest(BaseModel):
    message: str

@app.get("/")
async def root():
    return {"message": "AI Agent API is running. Visit /docs for API documentation."}

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    # Initialize the state with the user message
    inputs = {"messages": [HumanMessage(content=request.message)]}
    
    # Run the agent
    result = await agent.ainvoke(inputs)
    
    # Return the last message from the AI
    return {"response": result["messages"][-1].content}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)