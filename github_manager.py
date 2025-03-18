# git_manager.py

# Import the `os` module to interact with the operating system, such as working with file paths.
import os

# Import the `requests` library to send HTTP requests (e.g., GET, POST) to the GitHub API.
import requests

# Import a custom `logger` from a separate module (assumed to exist) to log messages for debugging and tracking.
from logger import logger

# Import `load_dotenv` from `dotenv` to load environment variables from a `.env` file, keeping sensitive data secure.
from dotenv import load_dotenv

class GitHubManager:
    """
    Manages interactions with the GitHub API, including repository creation, deletion, and template retrieval.

    This class provides a simple interface to perform operations on GitHub using its API. It requires a `.env` file
    with two variables: `GITHUB_PAT` (Personal Access Token) and `GITHUB_USERNAME`. If these credentials are missing
    or invalid, GitHub-related features will be disabled. The class also fetches templates like `.gitignore` files
    and license texts from GitHub.

    Attributes:
        token (str, optional): The GitHub Personal Access Token loaded from the `.env` file for authentication.
        username (str, optional): The GitHub username loaded from the `.env` file to identify the user.
        is_available (bool): A flag indicating if valid credentials were loaded (True) or not (False).
        headers (dict, optional): HTTP headers with the token for authenticated API requests, set only if credentials are valid.
    """

    def __init__(self):
        """
        Initializes a GitHubManager instance by loading credentials from a `.env` file and setting up API headers.

        This method locates the `.env` file in the same directory as this script, loads the GitHub credentials, and
        checks if they are valid. If credentials are present, it prepares headers for API requests. If not, it logs
        a warning and disables GitHub features.
        """
        # Get the directory where this script is located using `os.path.abspath(__file__)` to find the full path of this file.
        project_dir = os.path.dirname(os.path.abspath(__file__))

        # Construct the full path to the `.env` file by joining the project directory with the filename ".env".
        env_file_path = os.path.join(project_dir, ".env")

        # Log a debug message to show where the `.env` file is expected to be found.
        logger.debug(f"Attempting to load .env file from: {env_file_path}")

        # Load the `.env` file using `load_dotenv`. Returns True if successful, False otherwise.
        loaded = load_dotenv(env_file_path)

        # Check if the `.env` file failed to load and log a warning with instructions if it didn’t work.
        if not loaded:
            logger.warning(f"Could not load .env file at {env_file_path}. Please ensure it exists and contains GITHUB_PAT and GITHUB_USERNAME.")
        else:
            # Log a success message if the `.env` file was loaded.
            logger.debug(".env file loaded successfully")

            # Verify the file exists and log its contents for debugging (useful to check if variables are present).
            if os.path.exists(env_file_path):
                with open(env_file_path, "r") as f:
                    env_content = f.read()
                    logger.debug(f".env file contents: {env_content.strip()}")

        # Retrieve the GitHub Personal Access Token from environment variables using `os.getenv`.
        self.token = os.getenv("GITHUB_PAT")

        # Retrieve the GitHub username from environment variables.
        self.username = os.getenv("GITHUB_USERNAME")

        # Log whether the token was loaded and show the first 5 characters (if present) for security.
        logger.debug(f"GITHUB_PAT loaded: {self.token is not None}, value: {self.token[:5] + '...' if self.token else 'not set'}")

        # Log whether the username was loaded and show its value (or "not set" if missing).
        logger.debug(f"GITHUB_USERNAME loaded: {self.username is not None}, value: {self.username if self.username else 'not set'}")

        # Set `is_available` to True only if both token and username are present (converted to boolean with `bool()`).
        self.is_available = bool(self.token) and bool(self.username)

        # If credentials are missing, log a warning and GitHub features will be disabled.
        if not self.is_available:
            logger.warning("GitHub credentials not found; GitHub features will be disabled.")
        else:
            # If credentials are available, create HTTP headers for API requests with the token.
            self.headers = {
                'Authorization': f'token {self.token}',  # Token for authentication.
                'Accept': 'application/vnd.github.v3+json'  # Specifies the GitHub API version.
            }

    def get_language_templates(self):
        """
        Fetches a list of available `.gitignore` templates from the GitHub API.

        Returns:
            list: A list of `.gitignore` template names (e.g., "Python", "Java") if successful, or an empty list if it fails.

        This method checks if credentials are available, then sends a GET request to the GitHub API to retrieve all
        available `.gitignore` templates. It logs the result and handles errors gracefully.
        """
        # Check if GitHub credentials are set; if not, log a warning and return an empty list.
        if not self.is_available:
            logger.warning("Cannot fetch language templates; GitHub credentials are not set.")
            return []

        # Define the API endpoint for fetching `.gitignore` templates.
        url = "https://api.github.com/gitignore/templates"

        try:
            # Send a GET request to the API with headers and a 10-second timeout to avoid hanging.
            response = requests.get(url, headers=self.headers, timeout=10)

            # Raise an exception if the request fails (e.g., 404 or 500 status code).
            response.raise_for_status()

            # Parse the JSON response into a Python list of template names.
            templates = response.json()

            # Log how many templates were fetched and show the first 5 for reference.
            logger.info(f"Fetched {len(templates)} .gitignore templates from GitHub API: {templates[:5]}...")

            # Return the list of templates.
            return templates

        except requests.RequestException as e:
            # If an error occurs (e.g., network issue), log it and return an empty list as a fallback.
            logger.error(f"Failed to fetch GitHub templates: {e}. Falling back to empty list.")
            return []

    def get_license_templates(self):
        """
        Fetches a list of available license templates from the GitHub API.

        Returns:
            list: A list of dictionaries with license `key` and `name` (e.g., {"key": "mit", "name": "MIT License"}) if
                  successful, or an empty list if it fails.

        This method retrieves all license templates from GitHub, extracts their keys and names, and returns them in a
        simplified format. It includes error handling and logging.
        """
        # Check if credentials are available; if not, return an empty list.
        if not self.is_available:
            logger.warning("Cannot fetch license templates; GitHub credentials are not set.")
            return []

        # Define the API endpoint for fetching license templates.
        url = "https://api.github.com/licenses"

        try:
            # Send a GET request with headers and a timeout.
            response = requests.get(url, headers=self.headers, timeout=10)

            # Raise an exception if the request fails.
            response.raise_for_status()

            # Parse the JSON response and extract only the `key` and `name` fields from each license.
            licenses = [{"key": l["key"], "name": l["name"]} for l in response.json()]

            # Log the number of licenses fetched and show the first 5.
            logger.info(f"Fetched {len(licenses)} license templates from GitHub API: {licenses[:5]}...")

            # Return the list of licenses.
            return licenses

        except requests.RequestException as e:
            # Log any errors and return an empty list as a fallback.
            logger.error(f"Failed to fetch GitHub licenses: {e}. Falling back to empty list.")
            return []

    def get_license_content(self, license_key):
        """
        Fetches the full text content of a specific license template from the GitHub API.

        Args:
            license_key (str): The key of the license (e.g., "mit", "apache-2.0").

        Returns:
            str or None: The license text if successful, or None if it fails.

        This method retrieves the detailed content of a specific license based on its key.
        """
        # Check if credentials are available; if not, return None.
        if not self.is_available:
            logger.warning(f"Cannot fetch license content for '{license_key}'; GitHub credentials are not set.")
            return None

        # Construct the API URL for the specific license using the provided key.
        url = f"https://api.github.com/licenses/{license_key}"

        try:
            # Send a GET request to fetch the license content.
            response = requests.get(url, headers=self.headers, timeout=10)

            # Raise an exception if the request fails.
            response.raise_for_status()

            # Extract and return the "body" field from the JSON response, which contains the license text.
            return response.json()["body"]

        except requests.RequestException as e:
            # Log any errors and return None if the request fails.
            logger.error(f"Failed to fetch license content for '{license_key}': {e}")
            return None

    def get_gitignore_template(self, language):
        """
        Fetches the `.gitignore` template content for a specific programming language.

        Args:
            language (str): The name of the language (e.g., "Python", "Java").

        Returns:
            str or None: The `.gitignore` template text if successful, or None if it fails.

        This method retrieves the `.gitignore` content tailored to a specific language.
        """
        # Check if credentials are available; if not, return None.
        if not self.is_available:
            logger.warning("Cannot fetch .gitignore template; GitHub credentials are not set.")
            return None

        # Construct the API URL for the language-specific `.gitignore` template.
        url = f"https://api.github.com/gitignore/templates/{language}"

        try:
            # Send a GET request to fetch the template.
            response = requests.get(url, headers=self.headers, timeout=10)

            # Raise an exception if the request fails.
            response.raise_for_status()

            # Extract and return the "source" field from the JSON response, which contains the `.gitignore` text.
            return response.json()["source"]

        except requests.RequestException as e:
            # Log a warning if the request fails and return None.
            logger.warning(f"Failed to fetch {language} .gitignore template: {e}")
            return None

    def check_repository_exists(self, repo_name):
        """
        Checks if a repository exists under the user's GitHub account.

        Args:
            repo_name (str): The name of the repository to check.

        Returns:
            bool: True if the repository exists, False otherwise.

        This method sends a GET request to the repository URL and checks the response status.
        """
        # Check if credentials are available; if not, return False.
        if not self.is_available:
            logger.warning(f"Cannot check repository '{repo_name}'; GitHub credentials are not set")
            return False

        try:
            # Construct the URL for the specific repository using the username and repo name.
            response = requests.get(f"https://api.github.com/repos/{self.username}/{repo_name}", headers=self.headers, timeout=10)

            # Return True if the status code is 200 (OK), meaning the repository exists.
            return response.status_code == 200

        except Exception as e:
            # Log any errors and return False if the check fails.
            logger.error(f"Failed to check if repo '{repo_name}' exists: {e}")
            return False

    def delete_repository(self, repo_name):
        """
        Deletes a repository from the user's GitHub account.

        Args:
            repo_name (str): The name of the repository to delete.

        Returns:
            bool: True if the repository was deleted successfully, False otherwise.

        This method sends a DELETE request to remove the specified repository.
        """
        # Check if credentials are available; if not, return False.
        if not self.is_available:
            logger.warning(f"Cannot delete repository '{repo_name}'; GitHub credentials are not set")
            return False

        try:
            # Send a DELETE request to the repository URL.
            response = requests.delete(f"https://api.github.com/repos/{self.username}/{repo_name}", headers=self.headers, timeout=10)

            # Raise an exception if the request fails.
            response.raise_for_status()

            # Log success and return True if the repository is deleted.
            logger.info(f"Deleted GitHub repository '{repo_name}'")
            return True

        except Exception as e:
            # Log any errors and return False if the deletion fails.
            logger.error(f"Failed to delete repo '{repo_name}': {e}")
            return False

    def create_repository(self, repo_name, default_branch="main", private=False, license_template="mit"):
        """
        Creates a new repository on GitHub with the specified settings.

        Args:
            repo_name (str): The name of the repository to create.
            default_branch (str, optional): The default branch name (defaults to "main").
            private (bool, optional): Whether the repository should be private (defaults to False).
            license_template (str, optional): The license template to use (defaults to "mit").

        Returns:
            str or None: The URL of the created repository if successful, or None if it fails.

        This method sends a POST request to create a repository with a README and specified license.
        """
        # Check if credentials are available; if not, return None.
        if not self.is_available:
            logger.warning(f"Cannot create repository '{repo_name}'; GitHub credentials are not set")
            return None

        # Prepare the data payload for the POST request with repository settings.
        data = {
            "name": repo_name,              # Name of the repository.
            "private": private,             # Whether it’s private or public.
            "auto_init": True,              # Automatically initialize with a README and license.
            "default_branch": default_branch,  # Set the default branch name.
            "license_template": license_template  # Apply the chosen license.
        }

        try:
            # Send a POST request to create the repository.
            response = requests.post("https://api.github.com/user/repos", json=data, headers=self.headers, timeout=10)

            # Raise an exception if the request fails.
            response.raise_for_status()

            # Log the creation and return the repository URL.
            logger.info(f"Repo created: https://github.com/{self.username}/{repo_name}.git")
            return f"https://github.com/{self.username}/{repo_name}.git"

        except Exception as e:
            # Log the error with status code and response text, then return None.
            logger.error(f"GitHub API Error: {response.status_code} - {response.text}")
            return None

if __name__ == "__main__":
    """
    Runs a simple test of the GitHubManager class when this script is executed directly.

    This block demonstrates how to use the class by fetching templates and creating a test repository.
    """
    # Create an instance of GitHubManager.
    github = GitHubManager()

    # Fetch and print the available `.gitignore` templates.
    templates = github.get_language_templates()
    print("Language templates:", templates)

    # Fetch and print the available license templates.
    licenses = github.get_license_templates()
    print("License templates:", licenses)

    # Create a test repository with the MIT license and print its URL.
    repo_url = github.create_repository("test-repo", license_template="mit")
    print(f"Repository created at: {repo_url}")