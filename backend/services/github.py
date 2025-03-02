import logging
import base64
import os
from typing import Dict, Any, Optional
import requests

from backend.config import get_settings

# Configure logging
logger = logging.getLogger(__name__)

class GitHubService:
    """Service for interacting with GitHub."""
    
    def __init__(self):
        """Initialize the GitHub service."""
        self.settings = get_settings()
        self.token = self.settings.github_token
        self.owner = self.settings.github_owner
        self.repo = self.settings.github_repo
        self.base_url = f"https://api.github.com/repos/{self.owner}/{self.repo}"
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        logger.info(f"GitHub Service initialized for {self.owner}/{self.repo}")
    
    def get_file(self, path: str, ref: str = "main") -> Optional[Dict[str, Any]]:
        """
        Get file content from GitHub.
        
        Args:
            path: File path in the repository
            ref: Branch or commit reference
            
        Returns:
            File content and metadata or None if not found
        """
        url = f"{self.base_url}/contents/{path}?ref={ref}"
        
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            logger.info(f"File {path} not found in repository")
            return None
        else:
            logger.error(f"Error getting file {path}: {response.status_code} - {response.text}")
            response.raise_for_status()
    
    def create_or_update_file(self, path: str, content: str, commit_message: str, branch: str = "main") -> Dict[str, Any]:
        """
        Create or update a file in GitHub.
        
        Args:
            path: File path in the repository
            content: File content
            commit_message: Commit message
            branch: Branch name
            
        Returns:
            Response from GitHub API
        """
        url = f"{self.base_url}/contents/{path}"
        
        # Check if file already exists
        existing_file = self.get_file(path, branch)
        
        # Encode content
        encoded_content = base64.b64encode(content.encode()).decode()
        
        # Prepare request data
        data = {
            "message": commit_message,
            "content": encoded_content,
            "branch": branch
        }
        
        # Add sha if file exists (update)
        if existing_file:
            data["sha"] = existing_file["sha"]
            logger.info(f"Updating existing file {path}")
        else:
            logger.info(f"Creating new file {path}")
        
        # Make request
        response = requests.put(url, headers=self.headers, json=data)
        if response.status_code in (200, 201):
            return response.json()
        else:
            logger.error(f"Error creating/updating file {path}: {response.status_code} - {response.text}")
            response.raise_for_status()
    
    def create_branch(self, branch_name: str, base_branch: str = "main") -> Dict[str, Any]:
        """
        Create a new branch in GitHub.
        
        Args:
            branch_name: Name of the new branch
            base_branch: Base branch to create from
            
        Returns:
            Response from GitHub API
        """
        # Get the SHA of the latest commit on the base branch
        url = f"{self.base_url}/git/ref/heads/{base_branch}"
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            logger.error(f"Error getting reference for {base_branch}: {response.status_code} - {response.text}")
            response.raise_for_status()
        
        sha = response.json()["object"]["sha"]
        
        # Create the new branch
        url = f"{self.base_url}/git/refs"
        data = {
            "ref": f"refs/heads/{branch_name}",
            "sha": sha
        }
        
        response = requests.post(url, headers=self.headers, json=data)
        if response.status_code == 201:
            logger.info(f"Created new branch {branch_name} from {base_branch}")
            return response.json()
        elif response.status_code == 422:
            logger.warning(f"Branch {branch_name} already exists")
            return {"ref": f"refs/heads/{branch_name}", "object": {"sha": sha}}
        else:
            logger.error(f"Error creating branch {branch_name}: {response.status_code} - {response.text}")
            response.raise_for_status()
    
    def create_pull_request(self, title: str, body: str, head: str, base: str = "main") -> Dict[str, Any]:
        """
        Create a pull request in GitHub.
        
        Args:
            title: Pull request title
            body: Pull request description
            head: Source branch
            base: Target branch
            
        Returns:
            Response from GitHub API
        """
        url = f"{self.base_url}/pulls"
        data = {
            "title": title,
            "body": body,
            "head": head,
            "base": base
        }
        
        response = requests.post(url, headers=self.headers, json=data)
        if response.status_code == 201:
            logger.info(f"Created pull request: {title}")
            return response.json()
        else:
            logger.error(f"Error creating pull request: {response.status_code} - {response.text}")
            response.raise_for_status()
    
    def commit_and_push(self, code: str, file_path: str, commit_message: str, branch: str = "main") -> Dict[str, Any]:
        """
        Commit code to GitHub and optionally create a pull request.
        
        Args:
            code: Code to commit
            file_path: File path in the repository
            commit_message: Commit message
            branch: Branch to commit to
            
        Returns:
            Response with commit information
        """
        # Create branch if it doesn't exist
        if branch != "main":
            try:
                self.create_branch(branch)
            except requests.exceptions.HTTPError as e:
                if e.response.status_code != 422:  # Not "branch already exists"
                    raise
        
        # Commit the file
        result = self.create_or_update_file(
            path=file_path,
            content=code,
            commit_message=commit_message,
            branch=branch
        )
        
        return {
            "status": "success",
            "file_path": file_path,
            "branch": branch,
            "commit_url": result.get("commit", {}).get("html_url", ""),
            "file_url": result.get("content", {}).get("html_url", "")
        }