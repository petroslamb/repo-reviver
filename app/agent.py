# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import google.auth
from google.adk.agents import Agent
from google.adk.apps.app import App

from app.tools import (
    analyze_repo_structure,
    search_web,
    create_github_issue,
    create_pr_comment,
    generate_deployment_config,
    run_command
)
from app.instructions import (
    REPO_AUDITOR_INSTRUCTION,
    WEB_RESEARCHER_INSTRUCTION,
    PR_ADVISOR_INSTRUCTION,
    MAIN_AGENT_INSTRUCTION
)

_, project_id = google.auth.default()
os.environ.setdefault("GOOGLE_CLOUD_PROJECT", project_id)
os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "global")
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "True")

# --- Sub-Agents ---

repo_auditor = Agent(
    name="repo_auditor",
    model="gemini-2.5-flash",
    instruction=REPO_AUDITOR_INSTRUCTION,
    tools=[analyze_repo_structure, run_command],
)

web_researcher = Agent(
    name="web_researcher",
    model="gemini-2.5-flash",
    instruction=WEB_RESEARCHER_INSTRUCTION,
    tools=[search_web],
)

pr_advisor = Agent(
    name="pr_advisor",
    model="gemini-2.5-flash",
    instruction=PR_ADVISOR_INSTRUCTION,
    tools=[create_github_issue, create_pr_comment],
)

# --- Main Agent ---

root_agent = Agent(
    name="repo_reviver",
    model="gemini-2.5-flash",
    instruction=MAIN_AGENT_INSTRUCTION,
    tools=[
        analyze_repo_structure, # Can call directly or delegate
        generate_deployment_config,
        run_command
    ],
    sub_agents=[repo_auditor, web_researcher, pr_advisor],
)

app = App(root_agent=root_agent, name="app")
