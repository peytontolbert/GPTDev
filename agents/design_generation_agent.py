from chat.chat_with_ollama import ChatGPT
from base_agent import Agent

class DesignGenerationAgent(Agent):
    def __init__(self, name):
        super().__init__(name)
        self.gpt = ChatGPT()

    def generate_design(self, prompt):
        response = self.gpt.chat_with_ollama(prompt)
        return response

    def generate_design_from_code(self, code):
        prompt = f"Generate a design description for the following code: {code}"
        response = self.gpt.chat_with_ollama(prompt)
        return response

    def execute(self, input_data):
        generated_design = self.generate_design(input_data)
        self.save_to_file('generated_design.md', generated_design)

