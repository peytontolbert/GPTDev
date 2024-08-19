from agents.projectplanningagent import ProjectPlanningAgent
from datetime import datetime

# Create an instance of the ProjectPlanningAgent
project_name = "SampleProject"
start_date = datetime(2023, 10, 1)
planning_agent = ProjectPlanningAgent(project_name, start_date)

# Add tasks
planning_agent.add_task("Task 1", 5)
planning_agent.add_task("Task 2", 3)

# Add milestones
milestone_date = datetime(2023, 10, 10)
planning_agent.add_milestone("Milestone 1", milestone_date)

# Generate the project plan
planning_agent.generate_plan()
