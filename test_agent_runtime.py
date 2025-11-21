"""Test RepoReviver agent with a simple query."""
import asyncio
import os
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types

# Set minimal environment for testing
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "True")

async def test_agent():
    try:
        print("🚀 Testing RepoReviver Agent\n")
        
        # Import after setting environment
        from app.agent import root_agent
        
        print(f"✅ Agent loaded: {root_agent.name}")
        print(f"✅ Sub-agents: {', '.join([a.name for a in root_agent.sub_agents])}\n")
        
        # Create runner with proper app_name
        session_service = InMemorySessionService()
        runner = Runner(
            agent=root_agent,
            app_name="test_app",
            session_service=session_service
        )
        
        # Create query content
        query = "What sub-agents do you have and what do you do?"
        message_content = types.Content(
            role="user",
            parts=[types.Part.from_text(text=query)]
        )
        
        print(f"📤 Sending query: '{query}'\n")
        print("📥 Response:")
        print("-" * 60)
        
        # Run query using correct ADK API
        response_parts = []
        async for event in runner.run_async(
            user_id="test_user",
            session_id="test_session",
            new_message=message_content
        ):
            if event.is_final_response():
                if event.content and event.content.parts:
                    for part in event.content.parts:
                        if part.text:
                            response_parts.append(part.text)
                            print(part.text, end='', flush=True)
        
        print("\n" + "-" * 60)
        
        full_response = ''.join(response_parts)
        if len(full_response) > 0:
            print(f"\n✅ SUCCESS: Received {len(full_response)} character response")
            return True
        else:
            print("\n❌ FAILED: No response received")
            return False
            
    except Exception as e:
        print(f"\n❌ ERROR: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    result = asyncio.run(test_agent())
    print(f"\n{'='*60}")
    print(f"Test Result: {'✅ PASSED' if result else '❌ FAILED'}")
    print(f"{'='*60}")

