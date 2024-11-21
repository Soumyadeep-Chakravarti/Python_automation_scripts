import os
import subprocess
import sys


class GitSetupAutomation:
    """Automates the setup of dependencies for GitRepoInitAutomation."""

    @staticmethod
    def run_command(command, description):
        """Run a terminal command and print the result."""
        try:
            result = subprocess.run(command, check=True, text=True, capture_output=True)
            print(f"[INFO] {description} succeeded:\n{result.stdout.strip()}")
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] {description} failed:\n{e.stderr.strip()}")

    @staticmethod
    def detect_linux_distro():
        """Detect if the Linux system is Debian-based, Arch-based, or Fedora-based."""
        if os.path.exists("/etc/os-release"):
            with open("/etc/os-release", "r") as file:
                os_info = file.read().lower()
                if "debian" in os_info or "ubuntu" in os_info:
                    return "debian"
                elif "arch" in os_info:
                    return "arch"
                elif "fedora" in os_info or "rhel" in os_info:
                    return "fedora"
        print("[ERROR] Unable to detect Linux distribution.")
        return None

    @staticmethod
    def check_and_install_git():
        """Check if Git is installed, and install it if not."""
        try:
            subprocess.run(
                ["git", "--version"], check=True, capture_output=True, text=True
            )
            print("[INFO] Git is already installed.")
        except FileNotFoundError:
            print("[INFO] Git not found. Installing Git...")
            distro = GitSetupAutomation.detect_linux_distro()
            if distro == "debian":
                GitSetupAutomation.run_command(
                    ["sudo", "apt-get", "update"], "Updating package list"
                )
                GitSetupAutomation.run_command(
                    ["sudo", "apt-get", "install", "-y", "git"], "Installing Git"
                )
            elif distro == "arch":
                GitSetupAutomation.run_command(
                    ["sudo", "pacman", "-Sy", "--noconfirm", "git"], "Installing Git"
                )
            elif distro == "fedora":
                GitSetupAutomation.run_command(
                    ["sudo", "dnf", "install", "-y", "git"], "Installing Git"
                )
            else:
                print("[ERROR] Unsupported Linux distribution. Install Git manually.")

    @staticmethod
    def check_and_install_gh_cli():
        """Check if GitHub CLI (gh) is installed, and install it if not."""
        try:
            subprocess.run(
                ["gh", "--version"], check=True, capture_output=True, text=True
            )
            print("[INFO] GitHub CLI (gh) is already installed.")
        except FileNotFoundError:
            print("[INFO] GitHub CLI not found. Installing GitHub CLI...")
            distro = GitSetupAutomation.detect_linux_distro()
            if distro == "debian":
                GitSetupAutomation.run_command(
                    ["sudo", "apt-get", "install", "-y", "gh"], "Installing GitHub CLI"
                )
            elif distro == "arch":
                GitSetupAutomation.run_command(
                    ["sudo", "pacman", "-Sy", "--noconfirm", "github-cli"],
                    "Installing GitHub CLI",
                )
            elif distro == "fedora":
                GitSetupAutomation.run_command(
                    ["sudo", "dnf", "install", "-y", "gh"], "Installing GitHub CLI"
                )
            else:
                print(
                    "[ERROR] Unsupported Linux distribution. Install GitHub CLI manually."
                )

    @staticmethod
    def check_and_install_requests():
        """Check if the `requests` library is installed, and install it if not."""
        try:
            import requests  # noqa

            print("[INFO] Python `requests` library is already installed.")
        except ImportError:
            print("[INFO] Python `requests` library not found. Installing...")
            GitSetupAutomation.run_command(
                [sys.executable, "-m", "pip", "install", "requests"],
                "Installing requests",
            )

    @staticmethod
    def authenticate_gh_cli():
        """Authenticate GitHub CLI if not already authenticated."""
        try:
            result = subprocess.run(
                ["gh", "auth", "status"], check=True, capture_output=True, text=True
            )
            if "Logged in" in result.stdout:
                print("[INFO] GitHub CLI is already authenticated.")
            else:
                raise subprocess.CalledProcessError(1, "gh auth status")
        except subprocess.CalledProcessError:
            print("[INFO] Authenticating GitHub CLI...")
            GitSetupAutomation.run_command(
                ["gh", "auth", "login"], "Authenticating GitHub CLI"
            )

    @staticmethod
    def setup():
        """Run all setup tasks."""
        GitSetupAutomation.check_and_install_git()
        GitSetupAutomation.check_and_install_gh_cli()
        GitSetupAutomation.check_and_install_requests()
        GitSetupAutomation.authenticate_gh_cli()


if __name__ == "__main__":
    print("Starting setup process for GitRepoInitAutomation requirements...")
    GitSetupAutomation.setup()
    print("Setup process completed.")
