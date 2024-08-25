from agents.base_agent import Agent
import json

class CodeReviewAgent(Agent):
    def __init__(self, name):
        super().__init__(name)

    def execute(self, input_data):
        prompt = self.generate_prompt(input_data)
        response = self.gpt.chat_with_ollama(prompt, self.name)
        return self.parse_response(response)

    def generate_prompt(self, input_data):
        return (
            f"Review the following code:\n{input_data}\n\n"
            "Provide feedback based on the following criteria:\n"
            "1. Efficiency\n"
            "2. Readability\n"
            "3. Adherence to best practices\n"
            "4. Maintainability\n"
            "5. Security\n\n"
            "Provide a score for each criterion (out of 10) and suggest improvements if any."
        )
