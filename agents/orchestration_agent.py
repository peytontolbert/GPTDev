from base_agent import Agent
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
                results[task] = agent.execute(input_data)
        return results

    def parse_response(self, response):
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {"raw_response": response}

