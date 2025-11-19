import pytest
from app.agent import root_agent, repo_auditor, web_researcher, pr_advisor

def test_agent_initialization():
    """Verifies that the agents are initialized correctly."""
    assert root_agent.name == "repo_reviver"
    assert len(root_agent.sub_agents) == 3
    
    sub_agent_names = [agent.name for agent in root_agent.sub_agents]
    assert "repo_auditor" in sub_agent_names
    assert "web_researcher" in sub_agent_names
    assert "pr_advisor" in sub_agent_names

def test_tools_assignment():
    """Verifies that tools are assigned to the correct agents."""
    # Check Repo Auditor tools
    auditor_tools = [t.__name__ for t in repo_auditor.tools]
    assert "analyze_repo_structure" in auditor_tools
    
    # Check Web Researcher tools
    researcher_tools = [t.__name__ for t in web_researcher.tools]
    assert "search_web" in researcher_tools
    
    # Check PR Advisor tools
    advisor_tools = [t.__name__ for t in pr_advisor.tools]
    assert "create_github_issue" in advisor_tools
    assert "create_pr_comment" in advisor_tools
