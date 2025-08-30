from google.adk.agents import LlmAgent,LoopAgent

physicsexplainer = LlmAgent(
    name="PhysicsExplainer",
    description="This agent explains physics to students in simple terms",
    model="gemini-2.0-flash",
    instruction="""
You are an expert in physics education with over 20+ years of hands on experience. You have so many awards and publications.
Your task is to explain physics to students of all levels, from beginners to advanced learners, in simple terms.
Break the question into diffferent parts, explain them and at the end combine everything into a coherent answer.
Use analogies and real-world examples to make complex concepts easier to understand.
"""
)

refinement_loop = LoopAgent(
    name="RefinementLoop",      # Name of the Loop Agent
    description="This agent refines the explanations provided by the PhysicsExplainer agent",   #Description of the Loop Agent
    sub_agents=[physicsexplainer],       # The agents which needs to be in a loop
    max_iterations=3,        # Maximum number of iterations for the loop
)

root_agent = refinement_loop