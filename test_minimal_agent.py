"""Quick test script to verify agent can respond to queries."""
import asyncio
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.adk.agents import Agent
from google.adk.apps import App

# Create a minimal test agent WITHOUT MCP to avoid initialization delays
test_agent = Agent(
    name="test_agent",
    model="gemini-2.0-flash",
    instruction="You are a test agent. Just respond briefly to queries.",
    tools=[],
)

test_app = App(root_agent=test_agent, name="test_app")

async def test():
    print("Testing minimal agent...")
    session_service = InMemorySessionService()
    runner = Runner(
        app=test_app,
        session_service=session_service
    )
    
    print("Sending query...")
    session_id = await session_service.create_session()
    responses = []
    
    async for event in runner.run_async(session_id=session_id, user_message="Say hello in 5 words"):
        if hasattr(event, 'content') and event.content:
            responses.append(str(event.content))
    
    response = ''.join(responses)
    print(f"✅ Response: {response}")
    return len(response) > 0

if __name__ == "__main__":
    result = asyncio.run(test())
    print(f"\n{'✅ PASSED' if result else '❌ FAILED'}")

