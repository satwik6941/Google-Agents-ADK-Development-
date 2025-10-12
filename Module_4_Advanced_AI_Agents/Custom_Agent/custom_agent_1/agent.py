import logging
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

#Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#Session variables
APP_NAME = "sentiment_app"
USER_ID = "user_001"
SESSION_ID = "session_001"
MODEL = "gemini-2.0-flash"

# Declaration of Custom Agent 
class SentimentBasedAgent(LlmAgent):
    sentiment_analyser:LlmAgent
    positive_sentiment_responder:LlmAgent
    negative_sentiment_responder:LlmAgent

    model_config = {"arbitrary_types_allowed":True}

    def __init__(
        self,
        name: str,
        sentiment_analyser:LlmAgent,
        positive_sentiment_responder:LlmAgent,
        negative_sentiment_responder:LlmAgent
    ):
        sub_agents_list = [sentiment_analyser, positive_sentiment_responder, negative_sentiment_responder]

        super().__init__(
            name=name, 
            model=MODEL,
            sub_agents=sub_agents_list, 
            positive_sentiment_responder=positive_sentiment_responder,
            negative_sentiment_responder=negative_sentiment_responder,
            sentiment_analyser=sentiment_analyser,
            )
        

    @override
    async def _run_async_impl(self, ctx) -> AsyncGenerator[Event, None]:
        logger.info(f"[{self.name}] Starting sentiment-based workflow")
        
        logger.info(f"[{self.name}] Analyzing sentiment...")
        async for event in super()._run_async_impl(ctx):
            yield event
        
        sentiment = ctx.session.state.get("sentiment", "neutral")
        logger.info(f"[{self.name}] Detected sentiment: {sentiment}")

        if sentiment == "positive":
            logger.info(f"[{self.name}] Running positive responder...")
            async for event in self.positive_sentiment_responder.run_async(ctx):
                yield event
        elif sentiment == "negative":
            logger.info(f"[{self.name}] Running negative responder...")
            async for event in self.negative_sentiment_responder.run_async(ctx):
                yield event
        else:
            logger.info(f"[{self.name}] Neutral sentiment detected. No further action taken.")

        logger.info(f"[{self.name}] Workflow completed")
        

# Our Sub agents
sentiment_analyser = LlmAgent(
    name="Sentiment_Analyser",
    model=MODEL,
    description="Analyses the user sentiment and tell that it is positive or negative or neutral",
    instruction="""Analyze the sentiment of the user's message: {user_message}
Respond with ONLY one word: 'positive', 'negative', or 'neutral'""",
    output_key="sentiment"
)

positive_sentiment_responder = LlmAgent(
    name="Positive_Sentiment_Analyer",
    model=MODEL,
    description="Tell that it is positive sentiment",
    instruction="""Analyze the sentiment of the user's message: {user_message}
Write an encouraging response (2-3 sentences) that celebrates their positivity""",
    output_key="final_response"
)

negative_sentiment_responder = LlmAgent(
    name="Negative_Sentiment_Analyer",
    model=MODEL,
    description="Tell that it is negative sentiment",
    instruction="""Analyze the sentiment of the user's message: {user_message}
Write an empathetic response (2-3 sentences) that offers support and understanding.""",
    output_key="final_response"
)

sentiment_agent = SentimentBasedAgent(
    name="SentimentBasedAgent",
    sentiment_analyser=sentiment_analyser,
    positive_sentiment_responder=positive_sentiment_responder,
    negative_sentiment_responder=negative_sentiment_responder
)

async def user_sentiment_analysis(user_message: str):
    """Analyzes user sentiment and generates appropriate response"""
    # Create in-memory session service
    session_service = InMemorySessionService()
    
    # Set initial state with the user's message
    initial_state = {"user_message": user_message}

    # Create session with initial state - MUST USE AWAIT
    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
        state=initial_state
    )

    logger.info(f"Initial state: {session.state}")

    # Build the runner that orchestrates agent execution for the session.
    runner = Runner(
        agent=sentiment_agent,
        app_name=APP_NAME,
        session_service=session_service
    )

    # Wrap the user text in the SDK message container expected by the runner.
    new_message = types.Content(
        role="user",
        parts=[types.Part(text=user_message)],
    )

    # Stream events emitted by the runner and collect the final response
    agent_response = ""
    for event in runner.run(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=new_message,
    ):
        if event.is_final_response and event.content and event.content.parts:
            agent_response = event.content.parts[0].text
            print(f"Agent: {agent_response}")

    # Get final session state - MUST USE AWAIT
    final_session = await session_service.get_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
    )
    
    logger.info(f"Final state: {final_session.state}")

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
            asyncio.run(user_sentiment_analysis(user_message))
    
    main()
