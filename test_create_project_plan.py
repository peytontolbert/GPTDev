from agents.projectplanningagent import ProjectPlanningAgent

# Define a sample prompt and directory
sample_prompt = "Develop a web application for project management."
sample_directory = "./"

# Create an instance of ProjectPlanningAgent
agent = ProjectPlanningAgent(prompt=sample_prompt, directory=sample_directory)

# Call the create_project_plan method
agent.create_project_plan()

# Print the generated plan
if hasattr(agent, "plan"):
    print("Generated Plan:")
    print(agent.plan)
else:
    print("No plan was generated.")
