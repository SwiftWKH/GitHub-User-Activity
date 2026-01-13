# Implementation Guide

This guide explains how the GitHub Activity CLI code works under the hood.

## Code Structure

### 1. Imports and Setup

```python
import sys
import json
import urllib.request
```

- `sys`: Access command line arguments
- `json`: Parse GitHub API JSON responses
- `urllib.request`: Make HTTP requests to GitHub API

### 2. Data Fetching Function

```python
def fetch_github_activity(username):
    url = f"https://api.github.com/users/{username}/events"
    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read())
            return data
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None
```

**How it works:**
- Constructs GitHub API URL using f-string formatting
- Uses `urllib.request.urlopen()` to make HTTP GET request
- Reads response and parses JSON with `json.loads()`
- Returns parsed data or `None` if error occurs
- Handles network errors, invalid usernames, and API issues

### 3. Activity Display Function

```python
def display_activity(activity):
    if not activity:
        print("No activity found or an error occurred.")
        return
    
    for event in activity:
        event_type = event.get('type')
        repo_name = event.get("repo", {}).get("name", "unknown repo")
        # Event processing logic...
```

**How it works:**
- Checks if activity data exists
- Iterates through each event in the response
- Uses `.get()` method for safe dictionary access (prevents KeyError)
- Extracts event type and repository name
- Processes different event types with conditional logic

### 4. Event Type Processing

**PushEvent:**
```python
if event_type == 'PushEvent':
    payload = event.get('payload', {})
    commits = payload.get('commits', [])
    ref = payload.get('ref', '').replace('refs/heads/', '')
```
- Extracts commit information from payload
- Handles branch references by removing `refs/heads/` prefix
- Displays commit count or branch information

**IssuesEvent:**
```python
elif event_type == 'IssuesEvent' and event.get('payload', {}).get('action') == 'opened':
    print(f"Opened a new issue in {repo_name}")
```
- Checks both event type and action (only shows "opened" issues)
- Uses nested `.get()` calls for safe access

**WatchEvent:**
```python
elif event_type == 'WatchEvent':
    print(f"Starred {repo_name}")
```
- Simple case for repository starring events

### 5. Main Function and Entry Point

```python
def main():
    if len(sys.argv) != 2:
        print("Usage: python github_activity.py <username>")
        sys.exit(1)
    
    username = sys.argv[1]
    activity = fetch_github_activity(username)
    display_activity(activity)

if __name__ == "__main__":
    main()
```

**How it works:**
- Validates command line arguments (exactly 2: script name + username)
- Extracts username from `sys.argv[1]`
- Orchestrates the flow: fetch → display
- `if __name__ == "__main__"` ensures main() only runs when script is executed directly

## Key Programming Concepts

### Error Handling Strategy
- **Defensive programming**: Uses `.get()` instead of direct dictionary access
- **Graceful degradation**: Returns `None` on errors, continues execution
- **User feedback**: Prints meaningful error messages

### API Response Structure
GitHub events API returns an array of event objects:
```json
[
  {
    "type": "PushEvent",
    "repo": {"name": "user/repository"},
    "payload": {
      "commits": [...],
      "ref": "refs/heads/main"
    }
  }
]
```

### Safe Dictionary Access Pattern
```python
# Instead of: event['repo']['name'] (can cause KeyError)
# Use: event.get("repo", {}).get("name", "unknown repo")
```
This prevents crashes when expected fields are missing.

## Flow Diagram

1. **Input Validation** → Check command line arguments
2. **API Request** → Fetch user events from GitHub
3. **JSON Parsing** → Convert response to Python objects
4. **Event Processing** → Filter and format different event types
5. **Output Display** → Print formatted activity to terminal
