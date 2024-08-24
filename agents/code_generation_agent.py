from chat.chat_with_ollama import ChatGPT
from base_agent import Agent

class CodeGenerationAgent(Agent):
    def __init__(self, name):
        super().__init__(name)
        self.gpt = ChatGPT()

    def generate_code(self, requirements):
        prompt = f"Generate code for the following requirements: {requirements}"
        response = self.gpt.chat_with_ollama(prompt)
        return response

    def execute(self, input_data):
        generated_code = self.generate_code(input_data)
        self.save_to_file('generated_code.py', generated_code)

