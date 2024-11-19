import os
import subprocess
import platform


class GitRepository:
    """A class to represent and manage a Git repository."""

    def __init__(self, path):
        self.path = os.path.abspath(path)
        self.name = os.path.basename(self.path)

    def is_git_repo(self):
        """Check if the directory is a Git repository."""
        return os.path.isdir(os.path.join(self.path, ".git"))

    def run_git_command(self, command):
        """Run a Git command in this repository."""
        try:
            result = subprocess.run(
                command,
                cwd=self.path,
                text=True,
                capture_output=True,
                check=True,
                shell=True,  # Required for Windows compatibility
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"[{self.name}] Error running {command}:\n{e.stderr}")
            return None

    def fetch_updates(self):
        """Fetch updates from the remote repository."""
        print(f"[{self.name}] Fetching updates...")
        return self.run_git_command(["git", "fetch"])

    def check_uncommitted_changes(self):
        """Check for uncommitted or untracked changes."""
        print(f"[{self.name}] Checking for uncommitted changes...")
        status = self.run_git_command(["git", "status", "--porcelain"])
        return bool(status)

    def check_branch_status(self):
        """Check if the branch is ahead or behind the remote."""
        print(f"[{self.name}] Checking branch status...")
        result = self.run_git_command(
            ["git", "rev-list", "--left-right", "--count", "HEAD...@{u}"]
        )
        if result:
            ahead, behind = map(int, result.split())
            return ahead, behind
        return None, None

    def push_changes(self):
        """Push local changes to the remote repository."""
        print(f"[{self.name}] Pushing changes...")
        return self.run_git_command(["git", "push"])

    def pull_changes(self):
        """Pull changes from the remote repository."""
        print(f"[{self.name}] Pulling changes...")
        return self.run_git_command(["git", "pull", "--rebase"])

    def update(self):
        """Perform update operations: fetch, check, push, pull."""
        if not self.is_git_repo():
            print(f"[{self.name}] Not a Git repository. Skipping.")
            return

        if not self.fetch_updates():
            print(f"[{self.name}] Fetch failed. Skipping.")
            return

        if self.check_uncommitted_changes():
            print(f"[{self.name}] Uncommitted changes detected. Skipping.")
            return

        ahead, behind = self.check_branch_status()
        if ahead is None or behind is None:
            print(f"[{self.name}] Could not determine branch status. Skipping.")
            return

        if ahead > 0:
            print(f"[{self.name}] Local branch is ahead by {ahead} commits.")
            if not self.push_changes():
                print(f"[{self.name}] Push failed. Skipping.")
                return

        if behind > 0:
            print(f"[{self.name}] Local branch is behind by {behind} commits.")
            if not self.pull_changes():
                print(f"[{self.name}] Pull failed. Skipping.")
                return

        print(f"[{self.name}] Repository is up to date.")


class GitManager:
    """A class to manage multiple Git repositories."""

    def __init__(self, base_dir):
        self.base_dir = os.path.abspath(base_dir)
        self.repositories = []

    def discover_repositories(self):
        """Find all Git repositories in the base directory."""
        print("Discovering Git repositories...")
        for item in os.listdir(self.base_dir):
            repo_path = os.path.join(self.base_dir, item)
            if os.path.isdir(repo_path):
                repo = GitRepository(repo_path)
                if repo.is_git_repo():
                    self.repositories.append(repo)

    def update_all_repositories(self):
        """Update all discovered repositories."""
        print("=" * 60)
        print(f"Updating repositories in {self.base_dir}")
        print("=" * 60)
        for repo in self.repositories:
            repo.update()
        print("=" * 60)
        print("All repositories processed.")
        print("=" * 60)


if __name__ == "__main__":
    # Set the base directory (change this to your repositories directory)
    base_directory = os.path.expanduser("~/Desktop/Projects")

    # Adjust for Windows paths if necessary
    if platform.system() == "Windows":
        base_directory = "C:/Users/bunas/Desktop/Projects"

    # Create and run the Git manager
    manager = GitManager(base_directory)
    manager.discover_repositories()
    manager.update_all_repositories()
