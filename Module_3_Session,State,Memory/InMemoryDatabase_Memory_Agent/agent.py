"""This is a basic AI Agent code where we create an InMemorySessionService and InMemoryMemoryService, where we create and manage sessions, we also we update the state of the agent and we have temporary memory."""

import asyncio
from google.adk.sessions import InMemorySessionService
from google.adk.memory import InMemoryMemoryService
from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.genai.types import Content, Part
from dotenv import load_dotenv

load_dotenv()

# Identify the application, the user, and a session bucket to keep state.
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
    output_key="last_response",
)

# Create the in-memory session and memory services.
# Note: In-memory services does not have a persistent storage and are meant for testing and prototyping only. The data is lost when you restart the application.
session_service = InMemorySessionService()
memory_service = InMemoryMemoryService()

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
    # Connect the memory service so the agent can retrieve past context.
    runner = Runner(
        app_name=APP_NAME,
        agent=root_agent,
        session_service=session_service,
        memory_service=memory_service
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

        # Stream events emitted by the runner and print the final LLM response.
        response_text = ""
        for event in runner.run(
            user_id=USER_ID,
            session_id=SESSION_ID,
            new_message=new_message,
        ):
            if event.is_final_response and event.content and event.content.parts:
                response_text = event.content.parts[0].text
                print(f"Agent: {response_text}")

        # Store the conversation turn in memory for future reference.
        memory_content = f"User asked: {user_input}\nAgent replied: {response_text}"
        await memory_service.add_session_to_memory(session)

        # Reload the session so we can inspect and tweak the latest persisted state.
        session = await session_service.get_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id=SESSION_ID,
        )

        # Retrieve and display all memories stored for this user.
        memories = await memory_service.search_memory(
            app_name=APP_NAME,
            user_id=USER_ID,
            query=user_input
        )
        # Prints the memories but in a RAW format. (Helpful in understanding how the content is stored in the memory)
        print("\n=== Memory Contents ===")
        print(memories)

        # Show the user how the session state evolves after each turn.
        print("=== Current Session State ===")
        for key, value in session.state.items():
            print(f"{key}: {value}")
        print()

# Kick off the async workflow when executed as a script.
if __name__ == "__main__":
    asyncio.run(basic_in_memory_session())

