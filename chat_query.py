import requests
import json
import sys
import os

# File to store the current thread ID for conversation persistence
THREAD_FILE = ".chat_thread_id"

def load_thread_id():
    """Load the thread ID from file if it exists."""
    if os.path.exists(THREAD_FILE):
        with open(THREAD_FILE, 'r') as f:
            return f.read().strip()
    return None

def save_thread_id(thread_id):
    """Save the thread ID to file for future conversations."""
    with open(THREAD_FILE, 'w') as f:
        f.write(thread_id)

def clear_thread_id():
    """Clear the stored thread ID to start a new conversation."""
    if os.path.exists(THREAD_FILE):
        os.remove(THREAD_FILE)
        print("\033[93mCleared conversation history. Starting new conversation.\033[0m")
        print()

def query_chat_api(message, url="http://localhost:8000/chat", thread_id=None):
    """
    Send a message to the chat API and return the response.
    
    Args:
        message: The message to send to the API
        url: The API endpoint URL (default: http://localhost:8000/chat)
        thread_id: Optional thread ID to continue a conversation
    
    Returns:
        dict: The JSON response from the API
    """
    # Format the request body
    body = {"message": message}
    if thread_id:
        body["thread_id"] = thread_id
    
    try:
        # Submit the query via POST request
        response = requests.post(
            url,
            headers={"Content-Type": "application/json"},
            json=body
        )
        
        # Check if request was successful
        response.raise_for_status()
        
        # Parse the JSON response
        result = response.json()
        
        # Save thread ID for conversation continuity
        if "thread_id" in result:
            save_thread_id(result["thread_id"])
        
        # Print status
        print(f"\033[92mStatus: {response.status_code}\033[0m")
        if thread_id:
            print(f"\033[94mContinuing conversation (thread: {thread_id[:8]}...)\033[0m")
        else:
            print(f"\033[94mNew conversation started (thread: {result.get('thread_id', 'unknown')[:8]}...)\033[0m")
        print()
        
        return result
        
    except requests.exceptions.ConnectionError:
        print("\033[91mError: Could not connect to the API. Is the server running?\033[0m", file=sys.stderr)
        sys.exit(1)
    except requests.exceptions.HTTPError as e:
        print(f"\033[91mHTTP Error: {e}\033[0m", file=sys.stderr)
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"\033[91mError: {e}\033[0m", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError:
        print("\033[91mError: Could not parse API response as JSON\033[0m", file=sys.stderr)
        sys.exit(1)


def main():
    # Check for special commands
    if len(sys.argv) > 1 and sys.argv[1] == "--new":
        clear_thread_id()
        if len(sys.argv) > 2:
            message = " ".join(sys.argv[2:])
        else:
            print("Usage: python chat_query.py --new <message>")
            sys.exit(0)
    elif len(sys.argv) > 1:
        message = " ".join(sys.argv[1:])
    else:
        message = "Who will win the Super Bowl in 2026?"
    
    # Load existing thread ID if available
    thread_id = load_thread_id()
    
    # Query the API
    result = query_chat_api(message, thread_id=thread_id)
    
    # Display the response in a user-friendly format
    print("\033[96mResponse:\033[0m")
    if "response" in result:
        print(result["response"])
    else:
        # If response structure is different, print the entire result
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
