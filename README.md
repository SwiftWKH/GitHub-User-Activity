# GitHub User Activity CLI

A simple command line interface (CLI) that fetches and displays the recent activity of a GitHub user using the GitHub API. This project demonstrates working with APIs, handling JSON data, and building CLI applications.

## How It Works

The CLI uses Python's built-in libraries to:

1. **Fetch Data**: Makes HTTP requests to GitHub's public API endpoint (`https://api.github.com/users/{username}/events`)
2. **Parse Response**: Converts JSON response into Python data structures
3. **Display Activity**: Formats and displays different types of GitHub events

## Implementation Details

### Core Functions

- `fetch_github_activity(username)`: Makes API call and handles errors
- `display_activity(activity)`: Processes and formats different event types
- `main()`: Handles command line arguments and orchestrates the flow

### Supported Event Types

- **PushEvent**: Shows commits pushed to repositories
- **IssuesEvent**: Displays when new issues are opened
- **WatchEvent**: Shows when repositories are starred

### Error Handling

- Network connection issues
- Invalid usernames
- API rate limiting
- Missing data fields

## Usage

```bash
cd github-activity-cli
python github_activity.py <username>
```

Example:
```bash
python github_activity.py octocat
```

## Dependencies

Uses only Python standard library:
- `urllib.request` - HTTP requests
- `json` - JSON parsing
- `sys` - Command line arguments

No external packages required - runs with any Python 3 installation.

## Discoveries

- The GitHub Events API omits commit details for `PushEvent`. To show real commit counts, use the Compare endpoint: `/repos/{owner}/{repo}/compare/{before}...{head}`. The response includes `total_commits`, which reflects how many commits were pushed.
