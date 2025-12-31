# Quick Start Guide - Greenfield CyberSecurity Chatbot

Get the chatbot running in 3 simple steps!

## Prerequisites

- Python 3.8+
- OpenAI API key
- Tavily API key (optional, for search)

## Step 1: Install Dependencies

```bash
# Clone the repository (if you haven't already)
git clone https://github.com/rwfraser/2025PowerStack.git
cd 2025PowerStack

# Install Python dependencies
pip install -r requirements.txt
```

## Step 2: Configure API Keys

Create a `.env` file in the project root:

```bash
# Copy the example
cp .env.example .env

# Edit .env and add your keys
OPENAI_API_KEY=sk-proj-your-key-here
TAVILY_API_KEY=tvly-your-key-here  # Optional
```

**Get API Keys:**
- OpenAI: https://platform.openai.com/api-keys
- Tavily: https://tavily.com/ (optional, for search)

## Step 3: Start the Backend

```bash
python main.py
```

You should see:
```
Loaded OpenAI API key ending in: ...xyz123
Loaded Tavily API key ending in: ...abc789  # If configured
INFO: Uvicorn running on http://localhost:8000
```

## Using the Chatbot

You now have **three ways** to interact with Greenfield:

### Option 1: Web Interface (Recommended) 🌐

1. Open `frontend/index.html` in your browser
2. Or double-click the file
3. Start chatting with the beautiful UI!

**Features:**
- Modern, responsive design
- Real-time typing indicators
- Conversation memory
- Mobile-friendly

### Option 2: Command Line 💻

```bash
# Start a new conversation
python chat_query.py --new "Hello, I'm Alice"

# Continue the conversation
python chat_query.py "I need help with network security"

# End conversation
python chat_query.py "Good bye"
```

**Features:**
- Fast and lightweight
- Automatic conversation memory
- Color-coded output

### Option 3: API/Curl 🔧

```bash
# Send a message
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, my name is Bob"}'

# Continue conversation (save thread_id from response)
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is my name?", "thread_id": "abc-123-xyz"}'
```

**Features:**
- Direct API access
- Integrate with your apps
- Full REST API

## Quick Test

Try this conversation to test all features:

1. **Web Interface**: Open `frontend/index.html`
2. **Say Hello**: "Hi, I'm Sarah"
3. **Ask Question**: "What are ransomware best practices?"
4. **Test Memory**: "What's my name?"
5. **End Chat**: "Good bye"

You should see:
- ✅ Greenfield introduces itself
- ✅ Asks for your name
- ✅ Provides security advice (possibly using search)
- ✅ Remembers your name is Sarah
- ✅ Ends with "Thank you for using Greenfield"

## Project Structure

```
2025PowerStack/
├── main.py              # FastAPI backend server
├── agent.py             # LangGraph agent with memory & search
├── chat_query.py        # CLI interface
├── frontend/
│   ├── index.html       # Web interface
│   └── README.md        # Frontend docs
├── .env                 # Your API keys (create this)
├── checkpoints.db       # Conversation storage (auto-created)
└── requirements.txt     # Python dependencies
```

## Features Summary

✅ **Greenfield Persona** - Professional cybersecurity assistant  
✅ **Conversation Memory** - Remembers across messages  
✅ **Web Search** - Real-time info via Tavily (optional)  
✅ **Goodbye Handling** - Consistent conversation endings  
✅ **Multiple Interfaces** - Web, CLI, and API  
✅ **Modern UI** - TypeScript-style with Tailwind CSS  

## Common Issues

### Backend won't start

**Error**: `ModuleNotFoundError`
- **Solution**: Run `pip install -r requirements.txt`

**Error**: `OPENAI_API_KEY not found`
- **Solution**: Create `.env` file with your API key

### Frontend can't connect

**Error**: "Error connecting to server"
- **Solution**: Make sure backend is running on port 8000
- **Check**: Visit http://localhost:8000/docs

### Search not working

**Warning**: `TAVILY_API_KEY not found`
- **Solution**: Add Tavily key to `.env` (optional)
- **Note**: Chatbot works without search, just no real-time info

## Next Steps

📚 **Learn More:**
- [GREENFIELD_PERSONA.md](GREENFIELD_PERSONA.md) - Chatbot behavior
- [README_MEMORY.md](README_MEMORY.md) - Memory system
- [SEARCH_FUNCTIONALITY.md](SEARCH_FUNCTIONALITY.md) - Search features
- [frontend/README.md](frontend/README.md) - UI customization

🚀 **Customize:**
- Edit system prompt in `agent.py`
- Modify colors in `frontend/index.html`
- Add new endpoints in `main.py`

📦 **Deploy:**
- Backend: Railway, Heroku, AWS
- Frontend: GitHub Pages, Netlify, Vercel

## Support

Need help?
1. Check the logs in your terminal
2. Visit http://localhost:8000/docs for API documentation
3. Review the detailed documentation files
4. Check GitHub issues

## That's It! 🎉

You now have a fully functional AI cybersecurity chatbot with:
- Professional persona
- Conversation memory
- Web search capabilities
- Modern web interface
- CLI tools

**Happy chatting with Greenfield!** 🛡️
