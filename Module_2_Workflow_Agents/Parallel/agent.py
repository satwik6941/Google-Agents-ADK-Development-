from google.adk.agents import LlmAgent, ParallelAgent
from google.adk.tools import google_search

smartphonesagent = LlmAgent(
    name="SmartphonesAgent",
    description="This agent provides information about smartphones",
    model="gemini-2.0-flash",
    tools=[google_search],
    instruction="""
You are an expert in smartphones researching with over 20+ years experience. You have so many sources and networks to fid information.
Your task is to provide information about smartphones according to the query.
Use the google search to find more useful information.
"""
)

smartphonesresearch = LlmAgent(
    name="SmartphonesResearchAgent",
    description="This agent provides research-based information about smartphones and information about the companies that make them.",
    model="gemini-2.0-flash",
    tools=[google_search],
    instruction="""
You are an expert in smartphones researching with over 20+ years experience. You have so many sources and networks to fid information.
Your task is to provide information about smartphones according to the query. And also provide information of what the company is currently working on like what are they upto, what are the new tech they are developing etc kind of questions.
Use the google search to find more useful information.
"""
)

refinement = ParallelAgent(
    name="SmartphonesRefinementAgent",      # Name of the agent
    description="This agent gives the outputs by running the agents parallely.",     # Description of the agent
    sub_agents=[smartphonesagent, smartphonesresearch],       # The agents which needs to be exceuted in a parallel manner
)

root_agent = refinement