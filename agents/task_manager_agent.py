# agents/task_manager_agent.py

from agents.base_agent import Agent
from typing import List, Dict, Any
import json

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

    def dynamic_selection(self, agent_list: List[str], requirements: Dict[str, Any], prompt: str) -> List[str]:
        selection_prompt = (
            f"Given the following list of agents:\n{agent_list}\n\n"
            f"And the following requirements:\n{json.dumps(requirements, indent=2)}\n\n"
            "Select the most appropriate agents for the current task. "
            "Consider the agents' functionalities and how they can work together effectively to meet the given requirements."
        )
        selected_agents = self.gpt.chat_with_ollama(selection_prompt, prompt)
        return self.parse_response(selected_agents)