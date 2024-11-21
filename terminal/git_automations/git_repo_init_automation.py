import subprocess
import os


class GitRepoInitAutomation:
    """Automates the initialization of local and remote Git repositories."""

    @staticmethod
    def run_command(command, description):
        """Run a terminal command and print the result."""
        try:
            result = subprocess.run(command, check=True, text=True, capture_output=True)
            print(f"[INFO] {description} succeeded:\n{result.stdout}")
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] {description} failed:\n{e.stderr}")

    @staticmethod
    def create_local_repo(repo_name, directory="."):
        """
        Create a local Git repository.

        :param repo_name: Name of the repository
        :param directory: Directory where the repository should be created
        """
        path = os.path.join(directory, repo_name)
        try:
            os.makedirs(path, exist_ok=True)
            print(f"[INFO] Created directory: {path}")
            GitRepoInitAutomation.run_command(
                ["git", "init", path], f"Initializing Git repo in {path}"
            )
        except Exception as e:
            print(f"[ERROR] Could not create directory: {e}")

    @staticmethod
    def create_remote_repo(repo_name, private=True, token=None):
        """
        Create a remote GitHub repository using GitHub CLI or API.

        :param repo_name: Name of the repository
        :param private: Boolean indicating whether the repository should be private
        :param token: GitHub personal access token (required if API is used)
        """
        if token:
            import requests

            url = "https://api.github.com/user/repos"
            headers = {"Authorization": f"token {token}"}
            data = {"name": repo_name, "private": private}

            response = requests.post(url, json=data, headers=headers)
            if response.status_code == 201:
                print(f"[INFO] Remote repository '{repo_name}' created successfully.")
                print(f"URL: {response.json().get('html_url')}")
            else:
                print(
                    f"[ERROR] Failed to create remote repository: {response.json().get('message')}"
                )
        else:
            visibility = "private" if private else "public"
            GitRepoInitAutomation.run_command(
                ["gh", "repo", "create", repo_name, f"--{visibility}", "--confirm"],
                f"Creating remote GitHub repo '{repo_name}'",
            )

    @staticmethod
    def link_remote(repo_path, repo_url):
        """
        Link a local Git repository to a remote repository.

        :param repo_path: Path to the local repository
        :param repo_url: URL of the remote repository
        """
        GitRepoInitAutomation.run_command(
            ["git", "-C", repo_path, "remote", "add", "origin", repo_url],
            f"Linking local repo '{repo_path}' to remote '{repo_url}'",
        )

    @staticmethod
    def initialize_and_link(repo_name, directory=".", private=True, token=None):
        """
        Automate the full process: Create local repo, create remote repo, and link them.

        :param repo_name: Name of the repository
        :param directory: Directory where the repository should be created locally
        :param private: Boolean indicating whether the remote repository should be private
        :param token: GitHub personal access token (required for API-based remote creation)
        """
        GitRepoInitAutomation.create_local_repo(repo_name, directory)
        if (
            token
            or subprocess.run(["gh", "--version"], capture_output=True).returncode == 0
        ):
            GitRepoInitAutomation.create_remote_repo(repo_name, private, token)
            remote_url = f"https://github.com/YOUR_USERNAME/{repo_name}.git"  # Replace YOUR_USERNAME accordingly
            GitRepoInitAutomation.link_remote(
                os.path.join(directory, repo_name), remote_url
            )
        else:
            print(
                "[WARNING] Remote repo creation skipped. GitHub CLI or token is required."
            )
