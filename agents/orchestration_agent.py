from base_agent import Agent
from chat.chat_with_ollama import ChatGPT
import json

class OrchestrationAgent(Agent):
    def __init__(self, name, agents):
        super().__init__(name)
        self.agents = agents
        self.gpt = ChatGPT()

    def execute(self, input_data):
        task_plan = self.generate_task_plan(input_data)
        results = {}
        for task, agent_name in task_plan.items():
            agent = self.agents.get(agent_name)
            if agent:
                results[task] = agent.execute(input_data)
        return results

    def generate_task_plan(self, input_data):
        prompt = f"Given the input data: {input_data}, generate a task plan with specific agents to accomplish the tasks."
        response = self.gpt.chat_with_ollama(prompt)
        return self.parse_response(response)

    def parse_response(self, response):
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {"raw_response": response}

