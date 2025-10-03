"""This is a basic AI Agent code where we create an InMemorySessionService, where we create and manage sessions.
(There is no updation of the state and no memory involved in this code)."""

import asyncio
from google.adk.sessions import InMemorySessionService
from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

# Constants describing the app, user, and session identifiers.
APP_NAME = "coding_app"
USER_ID = "satwik"
SESSION_ID = "session_12345"

# Create a LLM agent that ADK will run as the root agent.
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

# Create an in-memory session service to track session state/events.
session_service = InMemorySessionService()

async def basic_in_memory_session() -> None:
    # Create a session and print the initial metadata.
    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
    )
    print("Session created successfully:")
    print(f"   Session ID: {session.id}")
    print(f"   App Name: {session.app_name}")
    print(f"   User ID: {session.user_id}")
    print(f"   Initial State: {session.state}")
    print(f"   Events (messages): {session.events}")
    print(f"   Last Update: {session.last_update_time}")
    print()

    # Build the runner that orchestrates agent execution for the session.
    runner = Runner(
        app_name=APP_NAME,
        agent=root_agent,
        session_service=session_service,
    )
    
    # Collect user input once for this demo and bail if nothing was typed.
    user_input = input("You: ").strip()
    if not user_input:
        print("No input provided.")
        return

    # Wrap the user text in the SDK message container expected by the runner.
    new_message = types.Content(
        role="user",
        parts=[types.Part(text=user_input)],
    )

    # Stream events emitted by the runner and print the final LLM response.
    for event in runner.run(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=new_message,
    ):
        if event.is_final_response and event.content and event.content.parts:
            print(f"Agent: {event.content.parts[0].text}")

# Run the async demo when the file is executed directly.
if __name__ == "__main__":
    asyncio.run(basic_in_memory_session())

