from agents.base_agent import Agent
from chat.chat_with_ollama import ChatGPT

class CodeGenerationAgent(Agent):
    def __init__(self, name):
        super().__init__(name)
        self.gpt = ChatGPT()

    def execute(self, input_data):
        generated_code = self.generate_code(input_data)
        self.save_to_file('generated_code.py', generated_code)

    def generate_code(self, requirements):
        prompt = self.generate_prompt(requirements)
        response = self.gpt.chat_with_ollama(prompt)
        return response

    def generate_prompt(self, input_data):
        return f"Generate code for the following requirements: {input_data}"

