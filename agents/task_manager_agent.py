# agents/task_manager_agent.py

from agents.base_agent import Agent
from typing import List, Dict, Any


class TaskManagerAgent(Agent):
    def __init__(self, name, agents: Dict[str, Agent]):
        super().__init__(name)
        self.agents = agents

    def execute_tasks(self, tasks: List[str], requirements: Dict[str, Any]) -> Dict[str, Any]:
        results = {}
        for task in tasks:
            agent = self.agents.get(task)
            if agent:
                results[task] = agent.execute(requirements)
        return results
