import pytest
from app.agent import root_agent
from app.codespace_tools import (
    create_codespace,
    run_in_codespace,
    delete_codespace,
    list_codespaces
)

def test_agent_initialization():
    """Verifies that the agent is initialized correctly."""
    assert root_agent.name == "repo_reviver"
    assert len(root_agent.tools) == 4  # 4 codespace tools
    assert root_agent.sub_agents is None or len(root_agent.sub_agents) == 0  # No sub-agents

def test_codespace_tools_available():
    """Verifies that all codespace tools are assigned to the agent."""
    tool_names = [t.__name__ for t in root_agent.tools]
    assert "create_codespace" in tool_names
    assert "run_in_codespace" in tool_names
    assert "delete_codespace" in tool_names
    assert "list_codespaces" in tool_names

def test_single_agent_architecture():
    """Verifies that we have a single-agent architecture (no delegation)."""
    # Root agent should have no sub-agents
    assert root_agent.sub_agents is None or len(root_agent.sub_agents) == 0
    # Root agent should have all tools directly
    assert len(root_agent.tools) == 4
    # This architecture avoids Gemini's multi-tool limitation

def test_tool_function_signatures():
    """Verifies that codespace tools have correct signatures."""
    # Test create_codespace signature
    import inspect
    sig = inspect.signature(create_codespace)
    assert "repo_url" in sig.parameters
    
    # Test run_in_codespace signature
    sig = inspect.signature(run_in_codespace)
    assert "codespace_name" in sig.parameters
    assert "commands" in sig.parameters
    
    # Test delete_codespace signature
    sig = inspect.signature(delete_codespace)
    assert "codespace_name" in sig.parameters

def test_no_code_executor():
    """Verifies that we are NOT using BuiltInCodeExecutor (local execution)."""
    # Ensure no code executor is assigned
    assert not hasattr(root_agent, 'code_executor') or root_agent.code_executor is None

def test_no_mcp_tools():
    """Verifies that we are NOT using MCP tools (avoids Gemini limitation)."""
    from google.adk.tools import McpToolset
    # Ensure no MCP tools in the agent
    for tool in root_agent.tools:
        assert not isinstance(tool, McpToolset)
