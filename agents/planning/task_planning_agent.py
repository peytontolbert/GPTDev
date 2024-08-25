from agents.base_agent import Agent
from chat.chat_with_ollama import ChatGPT
import json

class TaskPlanningAgent(Agent):
    def __init__(self, name):
        super().__init__(name)
        self.gpt = ChatGPT()

    def execute(self, input_data):
        return self.generate_task_plan(input_data)

    def generate_task_plan(self, input_data):
        prompt = f"Given the input data: {input_data}, generate a detailed task plan with specific agents to accomplish the tasks."
        response = self.gpt.chat_with_ollama(prompt)
        return self.parse_response(response)

    def parse_response(self, response):
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {"raw_response": response}

