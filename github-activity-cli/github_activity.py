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
    
def get_commit_count(username, push_id):
    """Fetch the actual commit count for a push event"""
    try:
        # Try to get commits from the GH API - using the push endpoint
        url = f"https://api.github.com/repos/owner/repo/commits?sha=head"
        # Since we don't have direct access to commit count from events API,
        # we'll use the 'size' from payload if available, or make a call to commits endpoint
        return None
    except:
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
            # The events API doesn't return commits array, but we can count them
            # by checking if there's a 'size' field or counting the distinct refs
            # For now, we'll make a secondary API call to get actual commit count
            push_id = payload.get('push_id')
            head = payload.get('head')
            before = payload.get('before')
            
            # Try to get commits from the commits API
            commit_count = get_commit_count_from_push(repo_name, before, head)
            
            if commit_count:
                print(f"- Pushed {commit_count} commit{'s' if commit_count != 1 else ''} to {repo_name}")
            else:
                # Fallback: use size from payload if available
                commits = payload.get('commits', [])
                commit_count = payload.get('size', len(commits))
                if commit_count == 0:
                    commit_count = 1  # At least 1 commit if there's a push
                print(f"- Pushed {commit_count} commit{'s' if commit_count != 1 else ''} to {repo_name}")
        
        elif event_type == 'IssuesEvent':
            payload = event.get('payload', {})
            if payload.get('action') == 'opened':
                print(f"- Opened a new issue in {repo_name}")

        elif event_type == 'WatchEvent':
            print(f"- Starred {repo_name}")

def get_commit_count_from_push(repo_name, before_sha, head_sha):
    """Get the actual number of commits in a push"""
    try:
        url = f"https://api.github.com/repos/{repo_name}/compare/{before_sha}...{head_sha}"
        req = urllib.request.Request(
            url,
            headers={
                "Accept": "application/vnd.github+json",
                "X-Github-Api-Version": "2022-11-28",
                "User-Agent": "github-activity-script"
            }
        )
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read())
            total_commits = data.get('total_commits', 0)
            return total_commits if total_commits > 0 else None
    except:
        return None


def main():
    if len(sys.argv) != 2:
        print("Usage: python github_activity.py <username>")
        sys.exit(1)
    
    username = sys.argv[1]
    activity = fetch_github_activity(username)
    display_activity(activity)

if __name__ == "__main__":
    main()
