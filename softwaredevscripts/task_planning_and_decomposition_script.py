from agents.planning.task_planning_agent import TaskPlanningAgent
from agents.planning.task_decomposition_agent import TaskDecompositionAgent
from agents.management.orchestration_agent import OrchestrationAgent

# Initializing the agents with the necessary configurations
task_planning_agent = TaskPlanningAgent("TaskPlanningAgent")
task_decomposition_agent = TaskDecompositionAgent("TaskDecompositionAgent")
orchestration_agent = OrchestrationAgent("OrchestrationAgent", {
    "task_planning_agent": task_planning_agent,
    "task_decomposition_agent": task_decomposition_agent
})

def automated_task_planning_and_decomposition(goal):
    # Step 1: Generate a task plan from the high-level goal
    task_plan = task_planning_agent.execute(goal)
    
    # Step 2: Decompose the tasks into smaller, manageable subtasks
    detailed_tasks = task_decomposition_agent.execute(task_plan)
    
    # Step 3: Orchestrate and delegate the tasks among other agents
    orchestration_agent.manage_workflow(detailed_tasks, None)  # Assuming `builder_gpt` is handled within

    return detailed_tasks

# Example usage
goal = "Develop a new feature for the software."
detailed_tasks = automated_task_planning_and_decomposition(goal)
print("Generated Task Plan:", detailed_tasks)
