import os
from typing import TypedDict, Annotated, Sequence
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.sqlite import SqliteSaver
from dotenv import load_dotenv
import sqlite3

# Load .env file and override any existing environment variables
load_dotenv(override=True)

# Validate API key at startup
api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    print(f"Loaded API key ending in: ...{api_key[-6:]}")
else:
    print("WARNING: OPENAI_API_KEY not found in environment")

# Define the state of our agent with memory support
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

# System prompt for cybersecurity customer support
SYSTEM_PROMPT = """You are an AI customer support chat bot for a cybersecurity firm. You will identify yourself at the start of each new conversation as Greenfield the CyberSecurity Professional and you will politely ask for the user's name. When they have provided their name to you, you will politely ask how you can help them with their cyber security request or concern. If you receive requests which do not seem to be related to the topic of cyber security you will politely request to refer them to a human agent.  Please refrain from identifying yourself as an AI entity during any conversation, as end users are already aware of this information."""

# Initialize the model with system prompt
model = ChatOpenAI(model="gpt-4o", temperature=0)

# Define the logic: a simple node that calls the LLM
def call_model(state: AgentState):
    messages = state['messages']
    
    # Add system prompt as the first message if this is a new conversation
    from langchain_core.messages import SystemMessage
    
    # Check if there's already a system message
    has_system_message = any(isinstance(msg, SystemMessage) for msg in messages)
    
    if not has_system_message:
        # Prepend system message for new conversations
        messages_with_system = [SystemMessage(content=SYSTEM_PROMPT)] + list(messages)
    else:
        messages_with_system = messages
    
    response = model.invoke(messages_with_system)
    return {"messages": [response]}

# Initialize SQLite connection and checkpointer for memory persistence
conn = sqlite3.connect("checkpoints.db", check_same_thread=False)
memory = SqliteSaver(conn)

# Define the Graph
workflow = StateGraph(AgentState)
workflow.add_node("agent", call_model)
workflow.set_entry_point("agent")
workflow.add_edge("agent", END)

# Compile the agent with memory checkpointer
agent = workflow.compile(checkpointer=memory)
