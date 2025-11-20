"""RepoReviver agent using GitHub Codespaces for cloud-based repository analysis."""

import os

from google.adk.agents import Agent
from google.adk.apps.app import App

# Configure Google Cloud environment (only if using Vertex AI)
# If using AI Studio, GOOGLE_GENAI_USE_VERTEXAI should be "False" and GOOGLE_API_KEY set in .env
use_vertexai = os.environ.get("GOOGLE_GENAI_USE_VERTEXAI", "True").lower() in ("true", "1", "yes")

if use_vertexai:
    import google.auth
    _, project_id = google.auth.default()
    os.environ.setdefault("GOOGLE_CLOUD_PROJECT", project_id)
    os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "global")

from app.codespace_tools import (
    create_codespace,
    run_in_codespace,
    delete_codespace,
    list_codespaces
)
from app.instructions import REPO_REVIVER_CODESPACE_INSTRUCTION

# Single agent with GitHub Codespaces tools
# This avoids Gemini's multi-tool limitation by having all tools on one agent
root_agent = Agent(
    name="repo_reviver",
    model=os.environ.get("REPO_REVIVER_MODEL", "gemini-2.5-flash"),
    instruction=REPO_REVIVER_CODESPACE_INSTRUCTION,
    description="Analyzes and revives GitHub repositories using cloud-based GitHub Codespaces",
    tools=[
        create_codespace,
        run_in_codespace,
        delete_codespace,
        list_codespaces
    ],
)

app = App(root_agent=root_agent, name="app")
