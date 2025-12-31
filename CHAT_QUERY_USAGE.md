# chat_query.py - Usage Guide

A command-line interface for chatting with the AI agent that supports **conversation memory**.

## Features

- **Persistent Conversation Memory**: Automatically maintains conversation context across multiple queries
- **Thread Management**: Stores thread ID in `.chat_thread_id` file for seamless conversation continuity
- **New Conversation Support**: Use `--new` flag to start fresh conversations

## Usage

### Basic Usage

Send a message to the AI:
```bash
python chat_query.py "Your message here"
```

### Continue a Conversation

The script automatically continues the previous conversation:
```bash
python chat_query.py "Hello, my name is Bob"
python chat_query.py "What is my name?"
# AI will remember: "Your name is Bob"
```

### Start a New Conversation

Clear conversation history and start fresh:
```bash
python chat_query.py --new "Hello, who are you?"
```

## Examples

### Example 1: Multi-turn Conversation
```bash
# First message
python chat_query.py "My favorite color is blue"
# Output: AI acknowledges your favorite color

# Follow-up (remembers context)
python chat_query.py "What's my favorite color?"
# Output: "Your favorite color is blue."
```

### Example 2: Starting Fresh
```bash
# Previous conversation exists
python chat_query.py "What did we talk about?"
# Output: AI responds with previous context

# Start new conversation
python chat_query.py --new "Hi there"
# Output: New conversation, no memory of previous chat
```

### Example 3: Default Message
```bash
# No arguments uses default message
python chat_query.py
# Output: Response to "Who will win the Super Bowl in 2026?"
```

## How It Works

1. **Thread Persistence**: Thread ID is stored in `.chat_thread_id` file
2. **Automatic Loading**: Each query loads the thread ID if it exists
3. **API Integration**: Sends thread_id with each request to maintain context
4. **Visual Feedback**: Shows whether continuing or starting a new conversation

## Output Format

The script provides colored output:
- 🟢 **Green**: HTTP status code
- 🔵 **Blue**: Thread information (new/continuing)
- 🟦 **Cyan**: AI response
- 🟡 **Yellow**: Conversation cleared message
- 🔴 **Red**: Error messages

## Files Created

- `.chat_thread_id`: Stores the current conversation thread ID
  - Automatically created on first message
  - Automatically updated with each response
  - Deleted when using `--new` flag

## Requirements

- Server must be running: `python main.py`
- Requires `requests` library: `pip install requests`

## Notes

- The `.chat_thread_id` file is local to the directory where you run the script
- Each directory can maintain its own separate conversation
- Thread IDs are UUIDs (e.g., `5ee7d7d4-1234-5678-9abc-def012345678`)
- Conversation history is stored in the server's `checkpoints.db` database
