"""Test script to verify API key configuration works."""
import os
import asyncio
from dotenv import load_dotenv

# Load .env file
load_dotenv()

async def test_api_key():
    """Test if the API key configuration works with a simple agent."""
    print("=" * 60)
    print("Testing RepoReviver API Key Configuration")
    print("=" * 60)
    
    # Show configuration (masked API key)
    api_key = os.environ.get("GOOGLE_API_KEY", "")
    use_vertexai = os.environ.get("GOOGLE_GENAI_USE_VERTEXAI", "True")
    model = os.environ.get("REPO_REVIVER_MODEL", "gemini-2.5-flash")
    
    print(f"\n📋 Configuration:")
    print(f"   Auth Mode: {'Vertex AI' if use_vertexai.lower() == 'true' else 'AI Studio (API Key)'}")
    print(f"   API Key: ***{api_key[-4:] if api_key else 'NOT SET'}")
    print(f"   Model: {model}")
    
    if not api_key and use_vertexai.lower() == 'false':
        print("\n❌ ERROR: GOOGLE_API_KEY not set but AI Studio mode is enabled!")
        return False
    
    print(f"\n🔄 Testing connection to {model}...")
    
    try:
        from google.adk.sessions import InMemorySessionService
        from google.adk.runners import Runner
        from google.genai import types
        from app.agent import root_agent
        
        # Create session service and runner (matching integration test pattern)
        session_service = InMemorySessionService()
        session = await session_service.create_session(
            app_name="test",
            user_id="test_user"
        )
        runner = Runner(agent=root_agent, session_service=session_service, app_name="test")
        
        # Create message content
        message = types.Content(
            role="user",
            parts=[types.Part.from_text(text="Reply with just 'Hello from RepoReviver!'")]
        )
        
        # Send test query
        responses = []
        async for event in runner.run_async(
            user_id=" test_user",
            session_id=session.id,
            new_message=message
        ):
            if hasattr(event, 'content') and event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        responses.append(part.text)
        
        response = ''.join(responses)
        
        if response:
            print(f"\n✅ SUCCESS! Agent responded:")
            print(f"   {response}")
            return True
        else:
            print("\n❌ FAILED: No response from agent")
            return False
            
    except Exception as e:
        print(f"\n❌ FAILED: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    result = asyncio.run(test_api_key())
    print("\n" + "=" * 60)
    print(f"Result: {'✅ API KEY WORKS!' if result else '❌ API KEY TEST FAILED'}")
    print("=" * 60)
    exit(0 if result else 1)
