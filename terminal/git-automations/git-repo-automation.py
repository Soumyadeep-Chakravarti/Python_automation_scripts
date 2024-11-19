import subprocess


class GitAutomation:
    """Class to automate Git commands with minimal space complexity."""

    @staticmethod
    def run_command(command, description):
        """Run a Git command and print the result."""
        try:
            result = subprocess.run(command, check=True, text=True, capture_output=True)
            print(f"[INFO] {description} succeeded:\n{result.stdout}")
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] {description} failed:\n{e.stderr}")

    @staticmethod
    def git_add():
        """Stage all changes."""
        GitAutomation.run_command(["git", "add", "."], "Adding changes")

    @staticmethod
    def git_commit(message):
        """Commit staged changes with a message."""
        GitAutomation.run_command(
            ["git", "commit", "-m", message], "Committing changes"
        )

    @staticmethod
    def git_push():
        """Push committed changes to the remote repository."""
        GitAutomation.run_command(["git", "push"], "Pushing changes")

    @staticmethod
    def git_pull():
        """Pull the latest changes from the remote repository."""
        GitAutomation.run_command(["git", "pull"], "Pulling latest changes")

    @staticmethod
    def git_create_branch(branch_name):
        """Create and switch to a new branch."""
        GitAutomation.run_command(
            ["git", "checkout", "-b", branch_name],
            f"Creating and switching to branch {branch_name}",
        )
