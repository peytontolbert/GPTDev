from agents.projectplanning_agent import ProjectPlanningAgent

prompt = "Create a new web application for task management."
directory = "project_plan"
name = "TaskManagement"
agent = ProjectPlanningAgent(prompt, directory, name)
agent.create_project_plan()
agent.generate_plan()
