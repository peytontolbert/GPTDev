from agents.base_agent import Agent
from chat.chat_with_ollama import ChatGPT

class UnitTestGenerationAgent(Agent):
    def __init__(self, name):
        super().__init__(name)
        self.gpt = ChatGPT()

    def generate_unit_tests(self, code):
        prompt = f"Generate unit tests for the following code: {code}"
        response = self.gpt.chat_with_ollama(prompt)
        return response

    def execute(self, input_data):
        unit_tests = self.generate_unit_tests(input_data)
        self.save_to_file('unit_tests.py', unit_tests)

