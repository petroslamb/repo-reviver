import subprocess
import json
from typing import Optional


def create_codespace(repo_url: str) -> dict:
    """Creates a GitHub Codespace for repository analysis.
    
    Args:
        repo_url: GitHub repository URL (e.g., petroslamb/resume-copilot or full URL)
    
    Returns:
        dict with codespace_name and status
    """
    try:
        # Extract owner/repo from URL if full URL provided
        if repo_url.startswith("http"):
            # https://github.com/owner/repo -> owner/repo
            repo_url = "/".join(repo_url.rstrip("/").split("/")[-2:])
        
        result = subprocess.run([
            'gh', 'codespace', 'create',
            '-R', repo_url,  # Use -R flag for repo
            '-m', 'basicLinux32gb',  # 2-core machine (true smallest/cheapest)
            '--retention-period', '1h',  # Auto-delete after 1 hour
        ], capture_output=True, text=True, check=True)
        
        # Extract codespace name from output (first line usually contains the name)
        codespace_name = result.stdout.strip().split('\n')[0] if result.stdout else None
        
        if not codespace_name:
            return {"status": "error", "error": "Failed to extract codespace name from output"}
        
        return {
            "status": "success",
            "codespace_name": codespace_name,
            "message": f"Codespace created: {codespace_name}"
        }
    except subprocess.CalledProcessError as e:
        return {"status": "error", "error": e.stderr}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def run_in_codespace(codespace_name: str, commands: str) -> dict:
    """Executes commands in a GitHub Codespace.
    
    Args:
        codespace_name: Name of the codespace
        commands: Shell commands to execute (multiline supported)
    
    Returns:
        dict with command output and status
    """
    try:
        # Pass commands via stdin to avoid quoting issues
        result = subprocess.run([
            'gh', 'codespace', 'ssh',
            '-c', codespace_name
        ], input=commands, capture_output=True, text=True, check=True, timeout=300)
        
        return {
            "status": "success",
            "output": result.stdout,
            "stderr": result.stderr if result.stderr else None
        }
    except subprocess.TimeoutExpired:
        return {"status": "error", "error": "Command timed out after 5 minutes"}
    except subprocess.CalledProcessError as e:
        return {
            "status": "error", 
            "error": e.stderr if e.stderr else "Command failed",
            "output": e.stdout if e.stdout else None
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}


def delete_codespace(codespace_name: str) -> dict:
    """Deletes a GitHub Codespace.
    
    Args:
        codespace_name: Name of the codespace to delete
    
    Returns:
        dict with deletion status
    """
    try:
        subprocess.run([
            'gh', 'codespace', 'delete',
            '-c', codespace_name,
            '--force'
        ], capture_output=True, text=True, check=True)
        
        return {
            "status": "success",
            "message": f"Deleted codespace: {codespace_name}"
        }
    except subprocess.CalledProcessError as e:
        return {"status": "error", "error": e.stderr if e.stderr else "Deletion failed"}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def list_codespaces() -> dict:
    """Lists all active codespaces for the authenticated user.
    
    Returns:
        dict with list of codespaces and their details
    """
    try:
        result = subprocess.run([
            'gh', 'codespace', 'list',
            '--json', 'name,repository,state,createdAt'
        ], capture_output=True, text=True, check=True)
        
        data = json.loads(result.stdout)
        return {
            "status": "success", 
            "codespaces": data,
            "count": len(data)
        }
    except subprocess.CalledProcessError as e:
        return {"status": "error", "error": e.stderr if e.stderr else "Failed to list codespaces"}
    except Exception as e:
        return {"status": "error", "error": str(e)}
