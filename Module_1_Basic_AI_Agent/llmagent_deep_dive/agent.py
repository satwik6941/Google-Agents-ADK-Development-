#Necessary Import Libraries
from google.adk.agents import LlmAgent
from google.adk.tools import google_search
from google.genai import types
from google.adk.planners import BuiltInPlanner,PlanReActPlanner
from pydantic import BaseModel

class mathsOutput(BaseModel):
    title: str
    description: str
    examples: list[str]


mathsagent = LlmAgent(
    name = "MathsAgent",  # Name of the agent
    description= "An agent specialized in solving mathematical problems.",   #Just a small one or 2 line description of the agent
    model= "gemini-2.0-flash",    # The model used by the agent
    instruction="""You are a helpful and expert agent who can answer any question related to mathematics.
    Explain the concept to the user by breaking it down into simple parts and simple terms.
    Use very simple examples to explain and slowly build up to more complex ideas.
    """,    #This is a system prompt for the agent, which means you tell the AI Agent how to behave and what is its character.
    tools=[google_search],   # This is an inbuilt tool named as "google_search" and now agent can access the web to give the responses

    # This is an optional configuration for content generation
    generate_content_config= types.GenerateContentConfig(
        max_output_tokens=2000,     # Maximum number of tokens to generate in the response
        temperature=0.2,  # Lower temperature for more focused and deterministic responses
    )
)

""" **IMPORTANT**:
If we are using a BaseModel or any custom tools, we cannot use them in combination with inbuilt tools like google search.
Example:
In the above agent we used google search because there was no tool declared nor used. But in the below agent there is a BaseModel being used and
in this point of time if we use google_search we can see an error message in the terminal. To verify this, you can try to use google_search in the mathsagent_basemodel and see the error.
"""

mathsagent_basemodel = LlmAgent(
    name = "MathsAgent",  # Name of the agent
    description= "An agent specialized in solving mathematical problems.",   #Just a small one or 2 line description of the agent
    model= "gemini-2.0-flash",    # The model used by the agent
    instruction="""You are a helpful and expert agent who can answer any question related to mathematics.
    Explain the concept to the user by breaking it down into simple parts and simple terms.
    Use very simple examples to explain and slowly build up to more complex ideas.
    Use the mathsOutput schema to format your responses.
    """,    #This is a system prompt for the agent, which means you tell the AI Agent how to behave and what is its character.  # This is an inbuilt tool named as "google_search" and now agent can access the web to give the responses
    output_schema=mathsOutput,  # This is an optional configuration to define the output schema of the agent, which means how exactly the output should look like

    # This is an optional configuration for content generation
    generate_content_config= types.GenerateContentConfig(
        max_output_tokens=2000,     # Maximum number of tokens to generate in the response
        temperature=0.2,  # Lower temperature for more focused and deterministic responses
    )
)

mathsagent_thinking = LlmAgent(
    name = "MathsAgent",  # Name of the agent
    description= "An agent specialized in solving mathematical problems.",   #Just a small one or 2 line description of the agent
    model= "gemini-2.5-flash",    # The model used by the agent
    instruction="""You are a helpful and expert agent who can answer any question related to mathematics.
    Explain the concept to the user by breaking it down into simple parts and simple terms.
    Use very simple examples to explain and slowly build up to more complex ideas.
    """,    #This is a system prompt for the agent, which means you tell the AI Agent how to behave and what is its character.
    planner=BuiltInPlanner(
        thinking_config=types.ThinkingConfig(
            include_thoughts=True,
            thinking_budget=1024,
        )
    ),          # This is an optional feature which only works for the Gemini 2.5 Family which will enable the agent to the thinking capabilities of the LLM.

    # This is an optional configuration for content generation
    generate_content_config= types.GenerateContentConfig(
        max_output_tokens=2000,     # Maximum number of tokens to generate in the response
        temperature=0.2,  # Lower temperature for more focused and deterministic responses
    )
)

mathsagent_reAct = LlmAgent(
    name = "MathsAgent",  # Name of the agent
    description= "An agent specialized in solving mathematical problems.",   #Just a small one or 2 line description of the agent
    model= "gemini-2.0-flash",    # The model used by the agent
    instruction="""You are a helpful and expert agent who can answer any question related to mathematics.
    Explain the concept to the user by breaking it down into simple parts and simple terms.
    Use very simple examples to explain and slowly build up to more complex ideas.
    Use the mathsOutput schema to format your responses.
    """,    #This is a system prompt for the agent, which means you tell the AI Agent how to behave and what is its character.  # This is an inbuilt tool named as "google_search" and now agent can access the web to give the responses
    planner=PlanReActPlanner(),     # This is a special tool called as ReACT reasoning which enables thinking even though the LLM does not have thinking capabilities

    # This is an optional configuration for content generation
    generate_content_config= types.GenerateContentConfig(
        max_output_tokens=2000,     # Maximum number of tokens to generate in the response
        temperature=0.2,  # Lower temperature for more focused and deterministic responses
    )
)

# While running the agents make sure to change this root_agent or else the agent which you want to work will not work
root_agent = mathsagent_thinking   #This is an agent declaration that this is the agent which needs to be executed, in simple terms in C or C++ programming language it is like a "main()"