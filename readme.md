README FILE FOR 2025PowerStack application:

1) add tavily search 
2) add memeory with langgraph-checkpoint-postgres and psycopg[binary,pool] in requirements.txt
3) add persistent memory with PostgresSaver

import os
from psycopg_pool import ConnectionPool
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.graph import StateGraph, START
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearchResults

# 1. Database Connection String (e.g., from Railway or local)
DB_URI = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost:5432/dbname")

# 2. Setup Tools & Model
search_tool = TavilySearchResults(max_results=2)
tools = [search_tool]
model = ChatOpenAI(model="gpt-4o").bind_tools(tools)

# 3. Initialize Postgres Connection Pool & Checkpointer
# autocommit=True is required for LangGraph to save state correctly
pool = ConnectionPool(conninfo=DB_URI, max_size=10, kwargs={"autocommit": True})

# This checkpointer will save the agent's state to Postgres
checkpointer = PostgresSaver(pool)

# NOTE: Run this once during startup to create the necessary tables
# checkpointer.setup() 

# 4. Define the Graph (same as before)
workflow = StateGraph(dict) # Simplified state for example
workflow.add_node("chatbot", lambda state: {"messages": [model.invoke(state["messages"])]})
workflow.add_node("tools", ToolNode(tools))
workflow.add_edge(START, "chatbot")
workflow.add_conditional_edges("chatbot", tools_condition)
workflow.add_edge("tools", "chatbot")

# 5. Compile with the checkpointer
agent = workflow.compile(checkpointer=checkpointer)


4) implement multi-user memory in main.py:

from fastapi import FastAPI
from pydantic import BaseModel
from agent import agent

app = FastAPI()

class ChatRequest(BaseModel):
    user_id: str  # Use this as the thread_id
    message: str

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    # This config tells LangGraph WHICH conversation history to load
    config = {"configurable": {"thread_id": request.user_id}}
    
    inputs = {"messages": [("user", request.message)]}
    
    # Run the agent with persistence
    result = await agent.ainvoke(inputs, config=config)
    
    return {"response": result["messages"][-1].content}

 5) add summarization in agent.py to control context window size:

from typing import Annotated
from langchain_core.messages import HumanMessage, SystemMessage, RemoveMessage
from langgraph.graph import MessagesState

# 1. Extend the state to include a 'summary' string
class State(MessagesState):
    summary: str

# 2. Define the logic to create a summary
def summarize_conversation(state: State):
    summary = state.get("summary", "")
    
    # If a summary already exists, we ask the LLM to update it with new info
    if summary:
        summary_message = (
            f"This is a summary of the conversation so far: {summary}\n\n"
            "Extend the summary with the new messages above."
        )
    else:
        summary_message = "Create a concise summary of the conversation above."

    # Add the summarization request to the message list
    messages = state["messages"] + [HumanMessage(content=summary_message)]
    response = model.invoke(messages)
    
    # We keep only the most recent 2 messages and delete the rest to save tokens
    # LangGraph uses RemoveMessage to physically clear them from the DB
    delete_messages = [RemoveMessage(id=m.id) for m in state["messages"][:-2]]
    
    return {"summary": response.content, "messages": delete_messages}

# 3. Create a logic gate: Should we summarize?
def should_continue(state: State):
    # If we have more than 6 messages, trigger summarization
    if len(state["messages"]) > 6:
        return "summarize_conversation"
    return END

# 4. Build the Graph
workflow = StateGraph(State)
workflow.add_node("chatbot", chatbot_node)
workflow.add_node("summarize_conversation", summarize_conversation)

workflow.add_edge(START, "chatbot")
# After the chatbot speaks, check if we need to summarize
workflow.add_conditional_edges("chatbot", should_continue)
workflow.add_edge("summarize_conversation", END)

agent = workflow.compile(checkpointer=checkpointer)



6) add next.js 15 + Shadcn frontend 

npx create-next-app@latest frontend --typescript --tailwind --eslint
# Settings: App Router (Yes), src/ directory (No), import alias (@/*) (Yes)

cd frontend
npm install lucide-react framer-motion

7) chat front end in typescript:

"use client";
import { useState, useEffect, useRef } from 'react';
import { Send, Bot, User, Loader2 } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

export default function ChatPage() {
  const [messages, setMessages] = useState<{role: string, content: string}[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    scrollRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim()) return;
    
    const userMsg = { role: 'user', content: input };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setIsLoading(true);

    try {
      const res = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: "local-user-1", message: input }),
      });
      const data = await res.json();
      setMessages(prev => [...prev, { role: 'assistant', content: data.response }]);
    } catch (error) {
      console.error("Failed to connect to backend", error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-zinc-50 text-zinc-900">
      {/* Header */}
      <header className="p-4 border-b bg-white flex items-center gap-2 font-bold">
        <Bot className="text-blue-600" /> 2025 AI Assistant
      </header>

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        <AnimatePresence>
          {messages.map((m, i) => (
            <motion.div 
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              key={i} 
              className={`flex gap-3 ${m.role === 'user' ? 'flex-row-reverse' : ''}`}
            >
              <div className={`p-1 rounded-full h-8 w-8 flex items-center justify-center ${m.role === 'user' ? 'bg-zinc-800 text-white' : 'bg-blue-100 text-blue-600'}`}>
                {m.role === 'user' ? <User size={16} /> : <Bot size={16} />}
              </div>
              <div className={`max-w-[80%] p-3 rounded-2xl ${m.role === 'user' ? 'bg-blue-600 text-white' : 'bg-white border shadow-sm'}`}>
                {m.content}
              </div>
            </motion.div>
          ))}
          {isLoading && (
            <div className="flex gap-3">
              <div className="bg-blue-100 text-blue-600 p-1 rounded-full h-8 w-8 flex items-center justify-center">
                <Loader2 size={16} className="animate-spin" />
              </div>
              <div className="bg-white border p-3 rounded-2xl italic text-zinc-400">Thinking...</div>
            </div>
          )}
        </AnimatePresence>
        <div ref={scrollRef} />
      </div>

      {/* Input Area */}
      <div className="p-4 bg-white border-t">
        <div className="max-w-3xl mx-auto flex gap-2">
          <input 
            className="flex-1 p-3 border rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Ask me anything..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
          />
          <button 
            onClick={sendMessage}
            className="bg-blue-600 text-white p-3 rounded-xl hover:bg-blue-700 transition-colors"
          >
            <Send size={20} />
          </button>
        </div>
      </div>
    </div>
  );
}

8) start backend: 

cd backend
source venv/bin/activate
uvicorn main:app --reload --port 8000

9) start frontend:  
cd frontend
npm run dev  

10) test local postgres:

psql -U postgres -c "CREATE DATABASE ai_memory;"

11) start backend

# Set your keys
set OPENAI_API_KEY=your_key
set TAVILY_API_KEY=your_key
set DATABASE_URL=postgresql://postgres:password@localhost:5432/ai_memory

# Run the server
uvicorn main:app --reload --port 8000

12)  start frontend:

npm run dev 

