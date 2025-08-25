from google.adk.agents import LlmAgent

first_agent = LlmAgent(
    name = "FirstAgent",         # Name of the agent
    model= "gemini-2.0-flash",   # Model to use (e.g., "gemini-2.0-flash", "gemini-2.5-pro.")
    description= "My first AI agent", # Just a small one line description of what agent does
    instruction="""You are a helpful and expert agent who can answer any question related to mathematics.
    Explain the concept to the user by breaking it down into simple parts and simple terms.
    Use very simple examples to explain and slowly build up to more complex ideas.
    """    #This is a system prompt for the agent, which means you tell the AI Agent how to behave and what is its character.
)

root_agent = first_agent        #This is an agent declaration that this is the agent which needs to be executed, in simple terms in C or C++ programming language it is like a "main()"