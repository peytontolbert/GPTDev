from agents.projectplanning_agent import ProjectPlanningAgent

prompt = "Create a new web application for task management."
directory = "./project_plan"

agent = ProjectPlanningAgent(prompt, directory)
agent.create_project_plan()
agent.generate_plan()
