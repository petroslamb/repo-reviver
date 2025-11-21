import subprocess
import os
from typing import Optional

def clone_repo(repo_url: str, target_dir: Optional[str] = None) -> dict:
    """Clones a GitHub repository locally.
    
    Args:
        repo_url: GitHub repository URL
        target_dir: Optional target directory (defaults to repo name)
    
    Returns:
        dict with status and path or error
    """
    try:
        if target_dir is None:
            repo_name = repo_url.rstrip('/').split('/')[-1].replace('.git', '')
            target_dir = f"/tmp/repo-reviver/{repo_name}"
        
        os.makedirs(os.path.dirname(target_dir), exist_ok=True)
        
        result = subprocess.run(
            ['git', 'clone', repo_url, target_dir],
            capture_output=True,
            text=True,
            check=True
        )
        
        return {
            "status": "success",
            "path": target_dir,
            "message": f"Successfully cloned to {target_dir}"
        }
    except subprocess.CalledProcessError as e:
        return {
            "status": "error",
            "error": e.stderr
        }

def create_branch(repo_path: str, branch_name: str) -> dict:
    """Creates and checks out a new git branch."""
    try:
        subprocess.run(
            ['git', 'checkout', '-b', branch_name],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True
        )
        return {"status": "success", "branch": branch_name}
    except subprocess.CalledProcessError as e:
        return {"status": "error", "error": e.stderr}

def commit_changes(repo_path: str, message: str) -> dict:
    """Stages all changes and commits them."""
    try:
        subprocess.run(['git', 'add', '.'], cwd=repo_path, check=True)
        subprocess.run(
            ['git', 'commit', '-m', message],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True
        )
        return {"status": "success", "message": message}
    except subprocess.CalledProcessError as e:
        return {"status": "error", "error": e.stderr}

def push_branch(repo_path: str, branch_name: str) -> dict:
    """Pushes the current branch to origin."""
    try:
        result = subprocess.run(
            ['git', 'push', 'origin', branch_name],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True
        )
        return {
            "status": "success",
            "branch": branch_name,
            "output": result.stdout
        }
    except subprocess.CalledProcessError as e:
        return {"status": "error", "error": e.stderr}

def read_file(repo_path: str, file_path: str) -> dict:

    """Reads a file from the repository."""
    try:
        full_path = os.path.join(repo_path, file_path)
        with open(full_path, 'r') as f:
            content = f.read()
        return {"status": "success", "content": content}
    except Exception as e:
        return {"status": "error", "error": str(e)}

def write_file(repo_path: str, file_path: str, content: str) -> dict:
    """Writes content to a file in the repository."""
    try:
        full_path = os.path.join(repo_path, file_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'w') as f:
            f.write(content)
        return {"status": "success", "path": file_path}
    except Exception as e:
        return {"status": "error", "error": str(e)}
