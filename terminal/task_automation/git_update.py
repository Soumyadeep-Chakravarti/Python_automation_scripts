import os
from .terminal.git_automations.git_repo_automation import GitAutomation
import subprocess


class GitRepository:
    """A class to represent and manage a Git repository."""

    def __init__(self, path):
        self.path = os.path.abspath(path)
        self.name = os.path.basename(self.path)

    def is_git_repo(self):
        """Check if the directory is a Git repository."""
        return os.path.isdir(os.path.join(self.path, ".git"))

    def fetch_updates(self):
        """Fetch updates from the remote repository."""
        print(f"[{self.name}] Fetching updates...")
        GitAutomation.run_command(["git", "fetch"], f"Fetching updates for {self.name}")

    def check_uncommitted_changes(self):
        """Check for uncommitted or untracked changes."""
        print(f"[{self.name}] Checking for uncommitted changes...")
        status = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=self.path,
            text=True,
            capture_output=True,
        ).stdout.strip()
        return bool(status)

    def check_branch_status(self):
        """Check if the branch is ahead or behind the remote."""
        print(f"[{self.name}] Checking branch status...")
        result = subprocess.run(
            ["git", "rev-list", "--left-right", "--count", "HEAD...@{u}"],
            cwd=self.path,
            text=True,
            capture_output=True,
        ).stdout.strip()
        ahead, behind = map(int, result.split()) if result else (0, 0)
        return ahead, behind

    def update(self):
        """Perform update operations: fetch, check, push, pull."""
        if not self.is_git_repo():
            print(f"[{self.name}] Not a Git repository. Skipping.")
            return

        self.fetch_updates()

        if self.check_uncommitted_changes():
            print(f"[{self.name}] Uncommitted changes detected. Skipping.")
            return

        ahead, behind = self.check_branch_status()
        if ahead or behind:
            if ahead > 0:
                print(
                    f"[{self.name}] Local branch is ahead by {ahead} commits. Pushing changes..."
                )
                GitAutomation.git_push()

            if behind > 0:
                print(
                    f"[{self.name}] Local branch is behind by {behind} commits. Pulling changes..."
                )
                GitAutomation.git_pull()
        else:
            print(
                f"[{self.name}] No changes to pull or push. Repository is up to date."
            )


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
    if os.name == "nt":
        base_directory = "C:/Users/bunas/Desktop/Projects"

    # Create and run the Git manager
    manager = GitManager(base_directory)
    manager.discover_repositories()
    manager.update_all_repositories()
