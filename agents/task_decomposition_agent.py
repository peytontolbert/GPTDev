from chat.chat_with_ollama import ChatGPT
import json
from agents.base_agent import Agent

class TaskDecompositionAgent(Agent):
    def __init__(self):
        super().__init__('TaskDecompositionAgent')

    def execute(self, input_data):
        prompt = self.generate_prompt(input_data)
        response = self.gpt.chat_with_ollama(prompt)
        return self.parse_response(response)

    def generate_prompt(self, input_data):
        return f"Break down the following task into smaller, manageable subtasks:\n{input_data}"

    def parse_response(self, response):
        return super().parse_response(response)
