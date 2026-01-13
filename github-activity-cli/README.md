# GitHub Activity CLI

## Implementation Guide

This guide will help you build a simple command line interface (CLI) to fetch and display the recent activity of a GitHub user using the GitHub API.

### Step 1: Set Up Your Project Directory

1. **Create a new directory for your project**:
   - Navigate to your workspace folder.
   - Create a new folder named `github-activity-cli`.

2. **Navigate into the project directory**:
   ```bash
   cd github-activity-cli
   ```

### Step 2: Create the Main Script File

1. **Create a new file named `github_activity.py`**:
   - This file will contain the main logic for your CLI application.

### Step 3: Write the Code

Open `github_activity.py` in your text editor and implement the following code:

```python
import sys
import json
import urllib.request

def fetch_github_activity(username):
    url = f"https://api.github.com/users/{username}/events"
    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read())
            return data
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def display_activity(activity):
    if not activity:
        print("No activity found or an error occurred.")
        return

    for event in activity:
        event_type = event.get('type')
        repo_name = event['repo']['name']
        if event_type == 'PushEvent':
            commits = len(event['payload']['commits'])
            print(f"Pushed {commits} commits to {repo_name}")
        elif event_type == 'IssuesEvent' and event['payload']['action'] == 'opened':
            print(f"Opened a new issue in {repo_name}")
        elif event_type == 'WatchEvent':
            print(f"Starred {repo_name}")
        # Add more event types as needed

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

### Step 4: Run Your CLI Application

1. **Open your terminal**.
2. **Navigate to your project directory**:
   ```bash
   cd path\to\github-activity-cli
   ```
3. **Run the application**:
   ```bash
   python github_activity.py <username>
   ```
   Replace `<username>` with the GitHub username you want to check.

### Step 5: Handle Errors Gracefully

- The code already includes basic error handling for network issues and invalid usernames. You can enhance it further by checking for specific HTTP status codes if needed.

### Step 6: Optional Enhancements

- Consider adding features like:
  - Filtering activity by event type.
  - Displaying activity in a more structured format.
  - Caching fetched data to improve performance.
  - Exploring other GitHub API endpoints for additional user information.

### Conclusion

By following this guide, you should be able to create a simple CLI application that fetches and displays a GitHub user's recent activity. Feel free to modify and expand upon the code as you see fit!