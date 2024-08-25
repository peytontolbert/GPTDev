from chat.chat_with_ollama import ChatGPT
import json
from agents.base_agent import Agent

class TaskDecompositionAgent(Agent):
    def __init__(self, name="TaskDecompositionAgent"):
        super().__init__(name)

    def execute(self, input_data):
        prompt = self.generate_prompt(input_data)
        response = self.gpt.chat_with_ollama(prompt)
        return self.parse_response(response)

    def generate_prompt(self, input_data):
        return (
            f"Given the following task:\n{input_data}\n\n"
            "Break this task down into smaller, manageable subtasks. "
            "Ensure that each subtask is clear and focused, making it easier to optimize or implement individually. "
            "Provide the output as a JSON object with subtasks as keys and descriptions as values."
        )
    def parse_response(self, response):
        return super().parse_response(response)
