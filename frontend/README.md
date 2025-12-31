# Greenfield CyberSecurity Chat - Frontend

A modern, responsive web interface for chatting with the Greenfield CyberSecurity AI assistant.

## Features

- 🎨 **Modern Design**: Clean, professional interface with Tailwind CSS
- 💬 **Real-time Chat**: Instant messaging with typing indicators
- 🧠 **Memory**: Conversations are remembered across messages
- 📱 **Responsive**: Works on desktop, tablet, and mobile
- ⚡ **Fast**: No build process required - just open and use
- 🔄 **New Chat**: Start fresh conversations anytime
- 🌙 **Dark Theme**: Professional cybersecurity-themed dark interface

## Quick Start

### 1. Start the Backend

Make sure the FastAPI backend is running:

```bash
# From the project root
python main.py
```

The server should start on `http://localhost:8000`

### 2. Open the Frontend

Simply open the HTML file in your browser:

**Option A: Double-click**
- Navigate to `frontend/index.html`
- Double-click to open in your default browser

**Option B: From command line**
```bash
# Windows
start frontend/index.html

# Or use a local server (optional)
python -m http.server 3000
# Then visit http://localhost:3000/frontend/
```

### 3. Start Chatting

- Type your cybersecurity question
- Press Enter or click Send
- Greenfield will respond with helpful information
- Your conversation is automatically saved

## Usage

### Starting a Conversation

1. The interface loads with a welcome message
2. Type your first message in the input field
3. Greenfield will introduce itself and ask for your name
4. Continue the conversation naturally

### Conversation Memory

- Each conversation gets a unique thread ID
- Messages are stored on the backend
- You can close and reopen the page - your conversation continues
- Click "New Chat" to start a fresh conversation

### Keyboard Shortcuts

- **Enter**: Send message
- **Shift + Enter**: (Future) New line in message

## Technical Details

### Stack

- **HTML5**: Semantic markup
- **Tailwind CSS**: Utility-first CSS framework (via CDN)
- **Vanilla JavaScript**: No framework dependencies
- **Fetch API**: Modern HTTP requests
- **SVG Icons**: Heroicons for clean vector graphics

### Architecture

```
Frontend (index.html)
    ↓ HTTP POST
Backend API (localhost:8000)
    ↓
LangGraph Agent
    ↓
OpenAI GPT-4o + Tavily Search
```

### API Integration

The frontend connects to these endpoints:

- `POST /chat` - Send message, receive response
- Thread IDs are managed automatically

### Features

**UI Components:**
- Gradient background with professional colors
- Animated message entrance
- Typing indicator with pulsing dots
- Auto-scroll to latest message
- Disabled send button while processing
- Error handling with user-friendly messages

**State Management:**
- Thread ID stored in memory
- Processing state prevents duplicate sends
- Message history maintained in DOM

## Customization

### Change API URL

Edit line 92 in `index.html`:

```javascript
const API_URL = 'http://localhost:8000';  // Change this
```

### Modify Colors

The interface uses Tailwind's color palette:
- Primary: Blue (600-700)
- Accent: Cyan (500-600)
- Background: Slate (700-900)

To customize, search for color classes in the HTML.

### Adjust Layout

The interface is responsive by default:
- Max width: 4xl (896px)
- Full height viewport
- Padding adapts to screen size

## Browser Support

Works in all modern browsers:
- ✅ Chrome/Edge (latest)
- ✅ Firefox (latest)
- ✅ Safari (latest)
- ✅ Mobile browsers

**Requirements:**
- JavaScript enabled
- Fetch API support (all modern browsers)

## Troubleshooting

### "Error connecting to server"

**Problem**: Frontend can't reach backend

**Solutions:**
1. Make sure backend is running: `python main.py`
2. Check backend is on port 8000
3. Verify CORS is enabled in `main.py`
4. Check browser console for detailed errors

### Messages not appearing

**Problem**: UI not updating

**Solutions:**
1. Check browser console for JavaScript errors
2. Refresh the page
3. Clear browser cache
4. Try a different browser

### Conversation not remembered

**Problem**: Each message starts fresh

**Solutions:**
1. Check backend has memory enabled
2. Verify `checkpoints.db` exists
3. Look for thread_id in network requests

## Development

### File Structure

```
frontend/
├── index.html       # Main chat interface
└── README.md        # This file
```

### Making Changes

The entire frontend is in one file for simplicity:
1. Edit `index.html`
2. Refresh browser
3. No build step needed

### Adding Features

Common additions:
- Message timestamps
- User avatars
- Code syntax highlighting
- File upload
- Voice input
- Message export

## Production Deployment

### Security Considerations

1. **CORS**: Update `main.py` to allow only your domain
   ```python
   allow_origins=["https://yourdomain.com"]
   ```

2. **HTTPS**: Always use HTTPS in production

3. **API URL**: Update to production backend URL

4. **Rate Limiting**: Add rate limiting to prevent abuse

### Hosting Options

**Static Hosting (Easy):**
- GitHub Pages
- Netlify
- Vercel
- CloudFlare Pages

**Full Stack Hosting:**
- Railway (backend + frontend)
- Heroku
- AWS/Azure/GCP

### Build Optimization (Optional)

For production, consider:
- Minify HTML/CSS/JS
- Use PostCSS for Tailwind optimization
- Add service worker for offline support
- Implement lazy loading

## License

Part of the 2025PowerStack project.

## Support

For issues or questions:
- Check backend logs
- Review browser console
- Test API endpoints directly
- Verify environment variables
