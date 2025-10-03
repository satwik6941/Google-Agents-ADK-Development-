"""This is a basic AI Agent code where we create an DatabaseSessionService, where we create and manage sessions, update the state and have a persistent storage (persistent memory).
Here we have the sessions and the chat history stored in the session are stored in memory (database)."""

import asyncio
import os
from google.adk.sessions import DatabaseSessionService
from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.genai import types
from dotenv import load_dotenv
import uuid
import traceback

load_dotenv()

# Using SQLite database for session persistence (Easiest - Local file database)
database_url = "sqlite:///./adk_sessions.db"
database_file = "./adk_sessions.db"

# Constants describing the app, user, and session identifiers.
APP_NAME = "coding_app"
USER_ID = "satwik"

# Create an LLM agent that ADK will run as the root agent.
root_agent = LlmAgent(
    name="coding_agent",
    model="gemini-2.0-flash",
    description="An agent that helps with coding tasks.",
    instruction=(
        "You are an expert and helpful coding assistant with many awards, publications, "
        "and research experience in the field of coding. Your task is to explain coding "
        "concepts and help with coding problems using simple language that a beginner can "
        "understand. Always break the concepts down into simple steps."
    ),
)

async def basic_database_session() -> None:
    session_id = None
    
    # Check if database file exists
    db_exists = os.path.exists(database_file)
    
    # Create a DatabaseSessionService to track session state/events.
    session_service = DatabaseSessionService(db_url=database_url)
    
    if db_exists:
        print("📁 Database found!")
        
        # Check for existing sessions
        try:
            # List all sessions for this app and user
            sessions_response = await session_service.list_sessions(
                app_name=APP_NAME,
                user_id=USER_ID
            )
            # Extract the actual list of sessions from the response
            existing_sessions = sessions_response.sessions
            
            if existing_sessions:
                # Get full session details to access events
                sessions_with_events = []
                for sess in existing_sessions:
                    # get_session() loads the complete session including all conversation history
                    full_session = await session_service.get_session(
                        app_name=APP_NAME,
                        user_id=USER_ID,
                        session_id=sess.id,
                    )
                    sessions_with_events.append(full_session)
                
                # Displays all the existing sessions with their details in the database
                print(f"\n✨ Found {len(sessions_with_events)} existing session(s):")
                for idx, sess in enumerate(sessions_with_events, 1):
                    print(f"   {idx}. Session ID: {sess.id}")
                    print(f"      Last updated: {sess.last_update_time}")
                    print(f"      Total messages: {len(sess.events)}")
                
                # User preference to continue or create new session
                print("\n📋 Options:")
                print("   1. Continue with an existing session")
                print("   2. Create a new session")
                choice = input("\nYour choice (1 or 2): ").strip()
                
                if choice == "1":
                    if len(sessions_with_events) == 1:
                        session_id = sessions_with_events[0].id
                        print(f"✅ Using session: {session_id}")
                    else:
                        session_num = input(f"Which session? (1-{len(sessions_with_events)}): ").strip()
                        try:
                            session_id = sessions_with_events[int(session_num) - 1].id
                            print(f"✅ Using session: {session_id}")
                        except (ValueError, IndexError):
                            print("❌ Invalid choice. Creating new session.")
                            session_id = None
                elif choice == "2":
                    session_id = None
                else:
                    print("❌ Invalid choice. Creating new session.")
                    session_id = None
            else:
                print("📭 No existing sessions found. Creating a new session.")
        except Exception as e:
            print(f"⚠️ Error checking sessions: {e}")
            traceback.print_exc()
            print("Creating a new session.")
    else:
        print("📭 No database found. Creating a new database and session.")
    
    # Create or retrieve session
    if session_id:
        # Use existing session - events are already loaded in session.events
        session = await session_service.get_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id=session_id,
        )
        print(f"\n✅ Retrieved existing session with {len(session.events)} messages:")
    else:
        # Create a new session with a unique ID
        # uuid.uuid4().hex[:8] generates an 8-character unique identifier
        session_id = f"session_{uuid.uuid4().hex[:8]}"
        session = await session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id=session_id,
        )
        print(f"\n✅ Session created successfully:")
    
    print(f"   Session ID: {session.id}")
    print(f"   App Name: {session.app_name}")
    print(f"   User ID: {session.user_id}")
    print(f"   Total messages: {len(session.events)}")
    print(f"   Last Update: {session.last_update_time}")
    print()

    # Build the runner that orchestrates agent execution for the session.
    runner = Runner(
        app_name=APP_NAME,
        agent=root_agent,
        session_service=session_service,
    )
    
    # Main conversation loop
    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue
        
        if user_input.lower() in ["quit", "exit", "q"]:
            print("👋 Goodbye!")
            break
        
        # Show conversation history if requested
        if user_input.lower() == "history":
            # Fetch fresh session to get latest events
            session = await session_service.get_session(
                app_name=APP_NAME,
                user_id=USER_ID,
                session_id=session.id,
            )
            print("\n" + "=" * 70)
            print("📜 CONVERSATION HISTORY (from database)")
            print("=" * 70)
            if session.events:
                for i, event in enumerate(session.events, 1):
                    if event.content and event.content.parts:
                        content = event.content.parts[0].text[:60]
                        role = event.author if event.author else "unknown"
                        print(f"{i}. [{role.upper()}]: {content}...")
            else:
                print("No conversation history yet.")
            print("=" * 70 + "\n")
            continue

        # Wrap the user text in the SDK message container expected by the runner.
        new_message = types.Content(
            role="user",
            parts=[types.Part(text=user_input)],
        )

        # Stream events emitted by the runner and print the final LLM response.
        for event in runner.run(
            user_id=USER_ID,
            session_id=session.id,
            new_message=new_message,
        ):
            if event.is_final_response and event.content and event.content.parts:
                print(f"Agent: {event.content.parts[0].text}\n")

# Run the async demo when the file is executed directly.
if __name__ == "__main__":
    asyncio.run(basic_database_session())

