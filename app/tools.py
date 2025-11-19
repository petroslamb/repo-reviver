import subprocess
import os
import json
from typing import List, Dict, Optional

def run_command(command: str) -> str:
    """Runs a shell command and returns the output."""
    try:
        result = subprocess.run(
            command, shell=True, check=True, capture_output=True, text=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error running command '{command}': {e.stderr}"

def analyze_repo_structure(repo_path: str = ".") -> str:
    """Analyzes the structure of the repository."""
    # List files
    files = run_command(f"find {repo_path} -maxdepth 2 -not -path '*/.*'")
    
    # Check for key files
    key_files = ["Dockerfile", "package.json", "requirements.txt", "go.mod", "pom.xml", "build.gradle", "Makefile", "README.md"]
    found_files = []
    for f in key_files:
        if os.path.exists(os.path.join(repo_path, f)):
            found_files.append(f)
            
    return f"Files found:\n{files}\n\nKey configuration files detected: {', '.join(found_files)}"

def search_web(query: str) -> str:
    """Simulates a web search for migration guidance."""
    # In a real scenario, this would call a search API.
    # For this demo, we'll return a placeholder or use a library if available.
    return f"Simulated search results for: {query}\n1. Official Documentation: https://example.com/docs\n2. StackOverflow: How to fix {query}..."

def create_github_issue(title: str, body: str, repo: Optional[str] = None) -> str:
    """Creates a GitHub issue using the gh CLI."""
    repo_flag = f"-R {repo}" if repo else ""
    cmd = f"gh issue create {repo_flag} --title '{title}' --body '{body}'"
    return run_command(cmd)

def create_pr_comment(pr_number: int, body: str, repo: Optional[str] = None) -> str:
    """Creates a comment on a GitHub PR using the gh CLI."""
    repo_flag = f"-R {repo}" if repo else ""
    cmd = f"gh pr comment {pr_number} {repo_flag} --body '{body}'"
    return run_command(cmd)

def generate_deployment_config(platform: str, app_name: str) -> str:
    """Generates a deployment configuration for the specified platform."""
    if platform.lower() == "cloud run":
        return f"""
# Cloud Run Deployment
gcloud run deploy {app_name} --source . --region us-central1 --allow-unauthenticated
"""
    elif platform.lower() == "github pages":
        return """
# GitHub Pages
1. Go to Settings > Pages
2. Select Source: GitHub Actions or Deploy from branch
"""
    elif platform.lower() == "defang":
        return f"""
# Defang
defang compose up
"""
    else:
        return "Unknown platform. Supported: Cloud Run, GitHub Pages, Defang."
