from typing import AsyncGenerator
from typing_extensions import override
from google.adk.agents import LlmAgent, BaseAgent
from google.adk.agents.invocation_context import InvocationContext
from google.genai import types
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.adk.events import Event
import asyncio
from dotenv import load_dotenv

load_dotenv()

# Session Variables
session_id = "session_002"
user_id = "satwik"
model = "gemini-2.0-flash"
app_name = "coding_review_app"

class CodingReviewAgent(LlmAgent):
    code_analyser:LlmAgent
    bug_fixer_agent:LlmAgent
    code_documenter_agent:LlmAgent

    model_config = {"arbitrary_types_allowed":True}

    def __init__(
        self,
        name:str,
        code_analyser:LlmAgent,
        bug_fixer_agent:LlmAgent,
        code_documenter_agent:LlmAgent
    ):
        sub_agents_list = [code_analyser, bug_fixer_agent, code_documenter_agent]

        super().__init__(
            name=name,
            model=model,
            sub_agents=sub_agents_list,
            code_analyser = code_analyser,
            bug_fixer_agent = bug_fixer_agent,
            code_documenter_agent = code_documenter_agent
        )
    
    @override
    async def _run_async_impl(self, ctx) -> AsyncGenerator[Event, None]:
        print("\n" + "="*60)
        print("Starting the coding review workflow...")
        print("="*60)

        # Run code_analyser first
        print("\n[Step 1] Running code analysis...")
        async for event in self.code_analyser.run_async(ctx):
            yield event

        # Get the analysis result from session state
        review = ctx.session.state.get("code_analysis", "").strip().lower()
        print(f"[Step 1] Analysis result: '{review}'")

        # Route based on analysis result
        if review == "bugs":
            print("\n[Step 2] Bugs detected! Initiating bug fixing...\n")
            async for event in self.bug_fixer_agent.run_async(ctx):
                yield event
            print("\n✅ Bug fixing completed.")
        elif review == "no_bugs_found":
            print("\n[Step 2] No bugs found. Generating documentation...\n")
            async for event in self.code_documenter_agent.run_async(ctx):
                yield event
            print("\n✅ Documentation completed.")
        else:
            print(f"\n⚠️ Unexpected analysis result: '{review}'. No further action taken.")

        print("\n" + "="*60)
        print("Coding review workflow completed.")
        print("="*60 + "\n")

code_analyser = LlmAgent(
    name="code_analyser",
    model=model,
    description="Analyses the code given as input by the user and checks if there are any bugs or not.",
    instruction="""You are expert coding analyser with 20+ years of experience.
    Your task is to analyse the input code provided by the user.

    IMPORTANT: Respond with EXACTLY one of these two words:
    - "bugs" (if you find any bugs, errors, or issues in the code)
    - "no_bugs_found" (if the code looks correct with no issues)
    
    Do not include any other text, explanations, or formatting. Just the single word.""",
    output_key="code_analysis"
)

bug_fixer_agent = LlmAgent(
    name="bug_fixer_agent",
    model=model,
    description="Fixes the bugs in the code given as input by the user.",
    instruction="""You are expert coding bug fixer with 20+ years of experience.
    Your task is to fix the bugs in the code provided by the user.
    
    Provide:
    1. A brief explanation of the bugs found
    2. The corrected code
    3. Explanation of what was fixed""",
    output_key="fixed_code"
)

code_documenter_agent = LlmAgent(
    name="code_documenter_agent",
    model=model,
    description="Documents the code given as input by the user.",
    instruction="""You are expert coding documenter with 20+ years of experience.
    Your task is to document the code provided by the user.
    
    Provide documentation with the following structure:
    1. Introduction - Brief overview of what the code does
    2. Tech Stack - Technologies, frameworks, and libraries used
    3. Detailed Explanation - Step-by-step breakdown of the code logic
    4. Conclusion - Summary and potential improvements""",
    output_key="code_documentation"
)

root_agent = CodingReviewAgent(
    name="code_review_agent",
    code_analyser=code_analyser,
    bug_fixer_agent=bug_fixer_agent,
    code_documenter_agent=code_documenter_agent
)

async def user_code_review(user_message: str):
    session_service = InMemorySessionService()
    
    # Set initial state with the user's message
    initial_state = {"user_message": user_message}

    # Create session with initial state - MUST USE AWAIT
    session = await session_service.create_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id,
        state=initial_state
    )

    # Build the runner that orchestrates agent execution for the session.
    runner = Runner(
        agent=root_agent,
        app_name=app_name,
        session_service=session_service
    )

    # Wrap the user text in the SDK message container expected by the runner.
    new_message = types.Content(
        role="user",
        parts=[types.Part(text=user_message)],
    )

    # Stream events emitted by the runner and collect the final response
    print("\n[Runner] Executing agent workflow...\n")
    for event in runner.run(
        user_id=user_id,
        session_id=session_id,
        new_message=new_message,
    ):
        if event.is_final_response and event.content and event.content.parts:
            agent_response = event.content.parts[0].text
            if agent_response and agent_response.strip():  # Only print if there's actual content
                print(f"\n📝 Final Response:\n{agent_response}\n")

    # Get final session state - MUST USE AWAIT
    final_session = await session_service.get_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id,
    )

# Run the async demo when the file is executed directly.
if __name__ == "__main__":
    def main():
        while True:
            user_message = input("You: ").strip()
            
            # Check for quit commands FIRST
            if user_message.lower() in ["q", "quit", "exit"]:
                print("👋 Exiting.")
                break
            
            # Check for empty input
            if not user_message:
                print("No input provided.")
                continue
            
            # Run the sentiment analysis
            asyncio.run(user_code_review(user_message))
    
    main()
