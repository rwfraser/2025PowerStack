# Quick Setup: Tavily Search

## Get Your Tavily API Key

To enable search functionality, you need a Tavily API key:

1. **Sign Up**: Visit [https://tavily.com/](https://tavily.com/)
2. **Create Account**: Sign up for a free account
3. **Get API Key**: Find your API key in the dashboard
4. **Add to .env**: Add the key to your `.env` file

## Configuration

Edit your `.env` file:

```bash
OPENAI_API_KEY=sk-proj-your-openai-key-here
TAVILY_API_KEY=tvly-your-tavily-key-here
```

## Verify Installation

Start the server:

```bash
python main.py
```

You should see:
```
Loaded OpenAI API key ending in: ...xyz123
Loaded Tavily API key ending in: ...abc789
```

If you see "WARNING: TAVILY_API_KEY not found", the search tool won't work.

## Test Search

Once configured, test with:

```bash
# Start server
python main.py

# In another terminal
python chat_query.py --new "What are the latest ransomware threats?"
```

The AI will search for current information and provide up-to-date results.

## Free Tier Limits

- **1,000 searches per month** on free tier
- Good for development and testing
- Upgrade to Pro for production use

## Next Steps

- Read [SEARCH_FUNCTIONALITY.md](SEARCH_FUNCTIONALITY.md) for detailed documentation
- Test different types of queries
- Monitor your usage on Tavily dashboard

## Troubleshooting

**Issue**: "TAVILY_API_KEY not found"
- **Solution**: Add the key to `.env` and restart the server

**Issue**: Search not working
- **Solution**: Check API key is correct on tavily.com dashboard

**Issue**: Rate limit errors
- **Solution**: You've exceeded 1,000 searches/month, upgrade or wait for reset
