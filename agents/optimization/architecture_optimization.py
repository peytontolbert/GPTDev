from chat.chat_with_ollama import ChatGPT
import json
from agents.base_agent import Agent

class ArchitectureOptimizationAgent(Agent):
    def __init__(self):
        super().__init__('ArchitectureOptimizationAgent')

    def execute(self, input_data):
        prompt = self.generate_prompt(input_data)
        response = self.gpt.chat_with_ollama(prompt)
        return self.parse_response(response)

    def generate_prompt(self, input_data):
        return f"Optimize the following project architecture for scalability and performance:\n{input_data}"

    def parse_response(self, response):
        return super().parse_response(response)
