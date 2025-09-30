"""This is a basic AI Agent code where we create an InMemorySessionService, where we create and manage sessions and also we update the state of the agent.
(There is no memory involved in this code)."""

import asyncio
from google.adk.sessions import InMemorySessionService
from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.genai.types import Content, Part
from dotenv import load_dotenv

load_dotenv()

# Identify the application, the user, and a session bucket to keep state.
APP_NAME = "coding_app"
USER_ID = "satwik"
SESSION_ID = "session_12345"

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
    output_key="last_response",
)

# Keep all sessions in memory for the lifetime of this process (no external store).
session_service = InMemorySessionService()

async def basic_in_memory_session() -> None:
    # Create a brand-new session with a starter state dictionary.
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

    # Wire up the runner that calls the agent and keeps the session in sync.
    runner = Runner(
        app_name=APP_NAME,
        agent=root_agent,
        session_service=session_service,
    )

    # Keep interacting until the user types q/quit.
    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue
        if user_input.lower() in {"q", "quit"}:
            print("Exiting conversation.")
            break

        # Wrap the user text in the SDK message container expected by the runner.
        new_message = Content(
            role="user",
            parts=[Part(text=user_input)],
        )

        ## Stream events emitted by the runner and print the final LLM response.
        for event in runner.run(
            user_id=USER_ID,
            session_id=SESSION_ID,
            new_message=new_message,
        ):
            if event.is_final_response and event.content and event.content.parts:
                print(f"Agent: {event.content.parts[0].text}")

        # Reload the session so we can inspect and tweak the latest persisted state.
        session = await session_service.get_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id=SESSION_ID,
        )

        # Maintain an explicit turn counter alongside the auto-managed last_response.
        session.state["turn_count"] = session.state.get("turn_count", 0) + 1

        # Show the user how the session state evolves after each turn.
        print("=== Current Session State ===")
        for key, value in session.state.items():
            print(f"{key}: {value}")
        print()

# Kick off the async workflow when executed as a script.
if __name__ == "__main__":
    asyncio.run(basic_in_memory_session())

