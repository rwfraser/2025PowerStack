import os
from typing import TypedDict, Annotated, Sequence
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from langchain_core.messages import BaseMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.prebuilt import ToolNode, tools_condition
from dotenv import load_dotenv
import sqlite3

# Load .env file and override any existing environment variables
load_dotenv(override=True)

# Validate API keys at startup
api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    print(f"Loaded OpenAI API key ending in: ...{api_key[-6:]}")
else:
    print("WARNING: OPENAI_API_KEY not found in environment")

tavily_key = os.getenv("TAVILY_API_KEY")
if tavily_key:
    print(f"Loaded Tavily API key ending in: ...{tavily_key[-6:]}")
else:
    print("WARNING: TAVILY_API_KEY not found - search functionality will not work")

# Define the state of our agent with memory support
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

# Initialize Tavily search tool for real-time information
search_tool = TavilySearch(max_results=3)
tools = [search_tool]

# System prompt for cybersecurity customer support
SYSTEM_PROMPT = """You are an AI customer support chat bot for a cybersecurity firm. You will identify yourself at the start of each new conversation as Greenfield the CyberSecurity Professional and you will politely ask for the user's name. When they have provided their name to you, you will politely ask how you can help them with their cyber security request or concern. If you receive requests which do not seem to be related to the topic of cyber security you will politely request to refer them to a human agent. Please refrain from identifying yourself as an AI entity during any conversation, as end users are already aware of this information.

You have access to a search tool that can look up current information about cybersecurity threats, vulnerabilities, best practices, and recent security news. Use this tool when you need up-to-date information or when answering questions about specific threats, CVEs, or recent security incidents.

IMPORTANT: When the user says "Good bye" (or variations like "Goodbye", "good-bye"), you must acknowledge their farewell and ALWAYS end your response with exactly: "Thank you for using Greenfield"""

# Initialize the model with system prompt and bind tools
model = ChatOpenAI(model="gpt-4o", temperature=0).bind_tools(tools)

# Define the logic: a simple node that calls the LLM
def call_model(state: AgentState):
    messages = state['messages']
    
    # Add system prompt as the first message if this is a new conversation
    from langchain_core.messages import SystemMessage, HumanMessage
    
    # Check if there's already a system message
    has_system_message = any(isinstance(msg, SystemMessage) for msg in messages)
    
    if not has_system_message:
        # Prepend system message for new conversations
        messages_with_system = [SystemMessage(content=SYSTEM_PROMPT)] + list(messages)
    else:
        messages_with_system = messages
    
    # Check if the last user message contains "Good bye" (case insensitive)
    last_user_message = None
    for msg in reversed(messages):
        if isinstance(msg, HumanMessage):
            last_user_message = msg.content.lower()
            break
    
    is_goodbye = False
    if last_user_message:
        # Check for variations of goodbye
        goodbye_variations = ["good bye", "goodbye", "good-bye", "goodby"]
        is_goodbye = any(variation in last_user_message for variation in goodbye_variations)
    
    response = model.invoke(messages_with_system)
    
    # Ensure proper ending for goodbye messages
    if is_goodbye:
        response_text = response.content
        closing_phrase = "Thank you for using Greenfield"
        
        # Check if the closing phrase is already present
        if closing_phrase not in response_text:
            # Add the closing phrase if not present
            if not response_text.endswith("."):
                response_text += "."
            response_text += f" {closing_phrase}"
            response.content = response_text
    
    return {"messages": [response]}

# Initialize SQLite connection and checkpointer for memory persistence
conn = sqlite3.connect("checkpoints.db", check_same_thread=False)
memory = SqliteSaver(conn)

# Define the Graph with tools
workflow = StateGraph(AgentState)
workflow.add_node("agent", call_model)
workflow.add_node("tools", ToolNode(tools))

workflow.set_entry_point("agent")

# Add conditional edges - if tools are called, go to tools node, otherwise end
workflow.add_conditional_edges(
    "agent",
    tools_condition,
)

# After tools are called, return to agent
workflow.add_edge("tools", "agent")

# Compile the agent with memory checkpointer
agent = workflow.compile(checkpointer=memory)
