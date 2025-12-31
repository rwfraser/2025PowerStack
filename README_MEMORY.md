# AI Agent Memory Functionality

This chatbot now includes persistent memory functionality using `langgraph-checkpoint-sqlite`.

## Features

- **Persistent Conversation Memory**: Conversations are stored in SQLite database (`checkpoints.db`)
- **Thread-based Management**: Each conversation has a unique thread ID
- **Automatic State Management**: LangGraph automatically saves/loads conversation state
- **Conversation History**: Retrieve past messages from any thread
- **Multi-conversation Support**: Handle multiple independent conversations simultaneously

## API Endpoints

### 1. Chat with Memory
**POST** `/chat`

Start or continue a conversation.

**Request:**
```json
{
  "message": "Hello, my name is Alice",
  "thread_id": "optional-thread-id"
}
```

**Response:**
```json
{
  "response": "Hello Alice! Nice to meet you.",
  "thread_id": "abc-123-xyz"
}
```

- If `thread_id` is omitted, a new conversation will be created
- If `thread_id` is provided, the conversation continues with full memory

### 2. Get Conversation History
**POST** `/history`

Retrieve all messages from a conversation thread.

**Request:**
```json
{
  "thread_id": "abc-123-xyz"
}
```

**Response:**
```json
{
  "thread_id": "abc-123-xyz",
  "messages": [
    {
      "type": "HumanMessage",
      "content": "Hello, my name is Alice"
    },
    {
      "type": "AIMessage",
      "content": "Hello Alice! Nice to meet you."
    }
  ]
}
```

### 3. New Conversation
**POST** `/new-conversation`

Generate a new thread ID for starting a fresh conversation.

**Response:**
```json
{
  "thread_id": "new-uuid-here",
  "message": "New conversation started"
}
```

## Usage Examples

### Example 1: Basic Conversation with Memory

```python
import requests

BASE_URL = "http://localhost:8000"

# Start new conversation
response = requests.post(f"{BASE_URL}/new-conversation")
thread_id = response.json()["thread_id"]

# First message
response = requests.post(
    f"{BASE_URL}/chat",
    json={"message": "My name is Alice", "thread_id": thread_id}
)
print(response.json()["response"])  # AI acknowledges the name

# Second message - AI should remember
response = requests.post(
    f"{BASE_URL}/chat",
    json={"message": "What is my name?", "thread_id": thread_id}
)
print(response.json()["response"])  # AI responds with "Alice"
```

### Example 2: Using curl

```bash
# Start new conversation
curl -X POST http://localhost:8000/new-conversation

# Chat with thread ID
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "My favorite color is blue", "thread_id": "YOUR-THREAD-ID"}'

# Test memory
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is my favorite color?", "thread_id": "YOUR-THREAD-ID"}'

# Get history
curl -X POST http://localhost:8000/history \
  -H "Content-Type: application/json" \
  -d '{"thread_id": "YOUR-THREAD-ID"}'
```

## Testing

Run the automated test script:

```bash
# Make sure the server is running first
python main.py

# In another terminal, run the test
python test_memory.py
```

## Memory Management Utilities

Use `memory_utils.py` for advanced memory management:

```python
from memory_utils import list_all_threads, delete_thread, get_thread_stats

# List all conversation threads
threads = list_all_threads()
print(f"Active threads: {threads}")

# Get statistics
stats = get_thread_stats()
print(f"Total conversations: {stats['total_threads']}")
print(f"Total checkpoints: {stats['total_checkpoints']}")

# Delete a specific conversation
deleted = delete_thread("abc-123-xyz")
print(f"Thread deleted: {deleted}")
```

## Database

Conversations are stored in `checkpoints.db` (SQLite database) in the project root directory.

- **Location**: `./checkpoints.db`
- **Format**: SQLite 3
- **Schema**: Managed automatically by `langgraph-checkpoint-sqlite`

To reset all conversations, simply delete the database file:
```bash
rm checkpoints.db
```

## Architecture

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │ HTTP Request (with thread_id)
       ▼
┌─────────────┐
│  FastAPI    │
│   main.py   │
└──────┬──────┘
       │ Pass config with thread_id
       ▼
┌─────────────┐
│  LangGraph  │
│   agent.py  │
└──────┬──────┘
       │ Load/Save state
       ▼
┌─────────────┐
│  SQLite     │
│Checkpointer │
└─────────────┘
```

## Configuration

The memory system requires no additional configuration. It automatically:
1. Creates the SQLite database on first use
2. Manages checkpoints for each conversation
3. Loads relevant conversation history when continuing a thread

## Notes

- Each thread maintains its own independent conversation history
- The AI remembers context only within the same thread
- Threads persist across server restarts
- Memory is stored locally in the SQLite database
