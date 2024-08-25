from agents.base_agent import Agent
from chat.chat_with_ollama import ChatGPT
import json
"""
Bug Tracking Agent: Integrates with bug tracking systems to manage and prioritize bug fixes.
"""
class BugTrackingAgent(Agent):
    def __init__(self, name):
        super().__init__(name)
        self.gpt = ChatGPT()

    def execute(self, input_data):
        return self.perform_task(input_data)

    def generate_prompt(self, input_data):
        return f"As a Bug Tracking Agent, manage and prioritize the following bug fixes:\n{input_data}\nProvide a detailed plan of action."

    def perform_task(self, input_data):
        prompt = self.generate_prompt(input_data)
        response = self.gpt.chat_with_ollama(prompt)
        return self.parse_response(response)

    def parse_response(self, response):
        try:
            result = json.loads(response)
        except json.JSONDecodeError:
            result = {"raw_response": response}
        return result

