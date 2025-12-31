# Search Functionality with Tavily

## Overview

Greenfield the CyberSecurity Professional is equipped with real-time web search capabilities using Tavily, enabling it to provide up-to-date information about cybersecurity threats, vulnerabilities, and best practices.

## Features

- **Real-time Information**: Access to current cybersecurity news and updates
- **Threat Intelligence**: Latest information on vulnerabilities and CVEs
- **Best Practices**: Current industry recommendations and standards
- **Security Incidents**: Recent security breach information
- **Automatic Tool Usage**: AI decides when to search based on query context

## Setup

### 1. Get Tavily API Key

1. Visit [https://tavily.com/](https://tavily.com/)
2. Sign up for a free account
3. Get your API key from the dashboard

### 2. Configure Environment

Add your Tavily API key to `.env`:

```bash
OPENAI_API_KEY=your_openai_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

### 3. Restart Server

```bash
python main.py
```

The server will confirm both API keys are loaded:
```
Loaded OpenAI API key ending in: ...xyz123
Loaded Tavily API key ending in: ...abc789
```

## How It Works

### Tool Integration

The agent uses LangGraph's tool calling system:
1. User asks a question
2. AI determines if web search is needed
3. If needed, calls Tavily search tool
4. Processes results and provides answer
5. Conversation continues normally

### Search Tool Configuration

```python
from langchain_tavily import TavilySearch

# Initialize with max 3 results per search
search_tool = TavilySearch(max_results=3)
```

### System Prompt Enhancement

The AI is instructed:
```
You have access to a search tool that can look up current information about 
cybersecurity threats, vulnerabilities, best practices, and recent security news. 
Use this tool when you need up-to-date information or when answering questions 
about specific threats, CVEs, or recent security incidents.
```

## Use Cases

### 1. Recent Threat Information

**User**: "What are the latest ransomware threats in 2025?"

**AI**: [Uses search tool] → Provides current ransomware trends and statistics

### 2. Specific Vulnerabilities

**User**: "Tell me about CVE-2024-12345"

**AI**: [Uses search tool] → Provides details about the specific CVE

### 3. Current Best Practices

**User**: "What are the latest password security recommendations?"

**AI**: [Uses search tool] → Provides current NIST or industry standards

### 4. Security News

**User**: "Have there been any major data breaches recently?"

**AI**: [Uses search tool] → Provides recent security incident information

### 5. General Advice

**User**: "How do I secure my home network?"

**AI**: [May or may not search] → Provides answer, searching if needed for current recommendations

## Technical Details

### Graph Structure

```
START → agent → [tools_condition] → tools → agent → END
                      ↓
                     END
```

**Flow:**
1. User message enters at agent node
2. Agent decides to use tools or respond directly
3. If tools are called, goes to tools node
4. Tool results return to agent
5. Agent synthesizes final response

### Code Implementation

**agent.py**:
```python
from langchain_tavily import TavilySearch
from langgraph.prebuilt import ToolNode, tools_condition

# Initialize tool
search_tool = TavilySearch(max_results=3)
tools = [search_tool]

# Bind tools to model
model = ChatOpenAI(model="gpt-4o").bind_tools(tools)

# Add tool node to graph
workflow.add_node("tools", ToolNode(tools))
workflow.add_conditional_edges("agent", tools_condition)
workflow.add_edge("tools", "agent")
```

## Examples

### Example 1: Search Triggered

```
User: "What are the top cybersecurity threats in 2025?"
AI: [Searches web] "Based on current reports, the top cybersecurity threats in 2025 include..."
[Provides detailed, up-to-date information]
```

### Example 2: No Search Needed

```
User: "How do I create a strong password?"
AI: "Here are best practices for creating strong passwords..."
[Provides answer from training without search]
```

### Example 3: CVE Lookup

```
User: "Tell me about Log4Shell"
AI: [Searches for current information] "Log4Shell (CVE-2021-44228) is a critical vulnerability..."
[Provides current mitigation strategies]
```

## Monitoring

### Server Output

When search is used, you'll see in the logs:
```
[Tool Call] TavilySearchResults: "latest ransomware 2025"
[Tool Result] Found 3 results...
```

### Debugging

To see when tools are called, check the conversation flow:
1. User message
2. AI tool call (if triggered)
3. Tool result
4. AI final response

## Benefits

1. **Accuracy**: Up-to-date information vs. static training data
2. **Relevance**: Current threats and recommendations
3. **Verification**: Can fact-check recent security news
4. **Comprehensiveness**: Combines AI knowledge with real-time data
5. **Automatic**: AI decides when search is beneficial

## Limitations

1. **API Rate Limits**: Tavily free tier has usage limits
2. **Search Quality**: Results depend on available web sources
3. **Context Window**: Search results use token budget
4. **Response Time**: Searches add latency to responses
5. **Cybersecurity Focus**: General enough to find cyber info, not hyper-specialized

## Best Practices

### For Users

- Ask specific questions for better search results
- Include dates when asking about recent events
- Be clear about what information you need

### For Developers

- Monitor API usage to stay within limits
- Adjust `max_results` based on needs (1-10)
- Consider caching frequent queries
- Log tool calls for analysis

## Troubleshooting

### "TAVILY_API_KEY not found" Warning

**Problem**: Search functionality won't work

**Solution**: 
1. Get API key from tavily.com
2. Add to `.env` file
3. Restart server

### Search Not Triggering

**Problem**: AI not using search when expected

**Solution**: 
- Make questions more specific
- Ask about recent events explicitly
- Verify API key is configured

### Slow Responses

**Problem**: Responses take longer with search

**Solution**:
- This is normal - search adds 1-3 seconds
- Reduce `max_results` if needed
- Consider async processing for production

## Configuration Options

### Adjust Results Count

```python
# Return more results (uses more tokens)
search_tool = TavilySearch(max_results=5)

# Return fewer results (faster, uses fewer tokens)
search_tool = TavilySearch(max_results=1)
```

### Search Parameters

Tavily supports additional parameters:
- `search_depth`: "basic" or "advanced"
- `include_domains`: List of domains to prioritize
- `exclude_domains`: List of domains to exclude

## API Costs

- **Tavily Free Tier**: 1,000 searches/month
- **Tavily Pro**: Higher limits and advanced features
- Check [tavily.com/pricing](https://tavily.com/pricing) for current rates

## Security Considerations

1. **API Key Security**: Keep Tavily API key in `.env` (not in code)
2. **Data Privacy**: Search queries are sent to Tavily
3. **Content Filtering**: Tavily results are from public web
4. **Rate Limiting**: Implement if exposing publicly

## Future Enhancements

Potential improvements:
- Custom search prompts for cybersecurity sources
- Result caching for common queries
- Multiple search tools for different data sources
- Search result quality scoring
- Fallback to training data if search fails
