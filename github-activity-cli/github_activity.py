import sys
import json
import urllib.request

def fetch_github_activity(username):
    url = f"https://api.github.com/users/{username}/events"

    req = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "X-Github-Api-Version": "2022-11-28",
            "User-Agent": "github-activity-script"
        }
    )

    try:
        with urllib.request.urlopen(req) as response:
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
        repo_name = event.get("repo", {}).get("name", "unknown repo")

        if event_type == 'PushEvent':
            payload = event.get('payload', {})
            commits = payload.get('commits', [])
            print(f"- Pushed {len(commits)} commit{'s' if len(commits) != 1 else ''} to {repo_name}")
        
        elif event_type == 'IssuesEvent':
            payload = event.get('payload', {})
            if payload.get('action') == 'opened':
                print(f"- Opened a new issue in {repo_name}")

        elif event_type == 'WatchEvent':
            print(f"- Starred {repo_name}")


def main():
    if len(sys.argv) != 2:
        print("Usage: python github_activity.py <username>")
        sys.exit(1)
    
    username = sys.argv[1]
    activity = fetch_github_activity(username)
    display_activity(activity)

if __name__ == "__main__":
    main()
