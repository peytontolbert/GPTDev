
from agents.base_agent import Agent
from chat.chat_with_ollama import ChatGPT
import json

class OrchestrationAgent(Agent):
    def __init__(self, name, agents):
        super().__init__(name)
        self.agents = agents
        self.gpt = ChatGPT()
        self.task_planning_agent = agents.get('task_planning_agent')

    def execute(self, input_data):
        task_plan = self.task_planning_agent.execute(input_data)
        results = {}
        for task, agent_name in task_plan.items():
            agent = self.agents.get(agent_name)
            if agent:
                try:
                    result = agent.execute(input_data)
                    results[task] = result
                    # Dynamically adjust tasks if necessary
                    self.adjust_task_flow(results, task, input_data)
                except Exception as e:
                    self.log(f"Error executing {agent_name}: {str(e)}")
                    # Implement fallback or retry mechanisms here
        return results

    def adjust_task_flow(self, results, task, input_data, task_plan):
        # Evaluate the result of the current task
        result = results[task]
        adjustments = []

        # Example 1: Add a new task if the current task result indicates an issue
        if "error" in result or "retry" in result:
            adjustments.append('error_handling')
        
        # Example 2: If a critical piece of information is missing, add a task to retrieve it
        if "missing_data" in result:
            adjustments.append('data_retrieval')
        
        # Example 3: If the task was successful, add a follow-up task
        if "follow_up" in result:
            adjustments.append('follow_up_analysis')

        # Add adjustments to the task plan
        for adj_task in adjustments:
            # You can add tasks dynamically based on the conditions
            task_plan[adj_task] = 'some_agent'  # Assign the appropriate agent

        # Example 4: If a task indicates a different sequence, reorder task_plan
        if "reorder_tasks" in result:
            reordered_tasks = self.reorder_tasks_based_on_result(task_plan)
            task_plan = reordered_tasks

    def reorder_tasks_based_on_result(self, task_plan):
        # Implement logic to reorder tasks based on certain conditions
        reordered_plan = {}
        # Reordering logic goes here...
        return reordered_plan

    def parse_response(self, response):
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {"raw_response": response}


    def manage_workflow(self, input_data, builder_gpt):
        # Determine which agents need to be run
        tasks = ['task_decomposition', 'knowledge_retrieval', 'code_review', 'meta_learning', 'exploration_strategy']
        task_plan = self.task_planning_agent.execute(input_data)
        #tasks = builder_gpt.task_manager_agent.determine_tasks(input_data)
        results = builder_gpt.task_manager_agent.execute_tasks(task_plan, input_data)
        # Handle dependencies, sequence, and error handling...
        return results