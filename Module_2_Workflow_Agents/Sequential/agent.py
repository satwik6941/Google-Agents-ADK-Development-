from google.adk.agents import LlmAgent,SequentialAgent
from google.adk.tools import google_search

physicsexplainer = LlmAgent(
    name="PhysicsExplainer",
    description="This agent explains physics to students in simple terms",
    model="gemini-2.0-flash",
    instruction="""
You are an expert in physics education with over 20+ years of hands on experience. You have so many awards and publications.
Your task is to explain physics to students of all levels, from beginners to advanced learners, in simple terms.
Break the question into diffferent parts, explain them and at the end combine everything into a coherent answer.
Use analogies to make complex concepts easier to understand.
""",
    output_key="physics"        # This is like a variable kind of thing which stores the agent output in it. This is very similar to how we declare a=3 in python which means 3 is stored in "a". Now in similar manner the agent output is stored in the "physics".
)

casestudyagent = LlmAgent(
    name="CaseStudyAgent",
    description="This agent provides real-world case studies to illustrate physics concepts",
    model="gemini-2.0-flash",
    tools=[google_search],
    instruction="""
You are an expert in physics education with over 20+ years of hands on experience. You have so many awards and publications.

Here is the topic of the physics which user is asking to explain: {physics}

Your task is to give real life examples to students of all levels, from beginners to advanced learners, in simple terms.
Use google search to find good examples.
"""
)

"""The output of the above physicsexplaineragent is access by the casestudyagent by using the {physics} variable. 
<example>
Here is the topic of the physics which user is asking to explain: {physics}
</example>
This part in the casestudy agent helps in taking the output of the PhysicsExplainer agent and using it as context for finding relevant case studies.
"""

refinement = SequentialAgent(
    name="Refinement",      # Name of the Sequential Agent
    description="This agent runs the agents in a sequential manner to refine the explanations provided by the PhysicsExplainer agent",   # Description of the Sequential Agent
    sub_agents=[physicsexplainer, casestudyagent],       # The agents which needs to be exceuted in a sequential manner
)

root_agent = refinement