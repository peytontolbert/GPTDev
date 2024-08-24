from chat.chat_with_ollama import ChatGPT
from base_agent import Agent

class DocumentationGenerationAgent(Agent):
    def __init__(self, name):
        super().__init__(name)
        self.gpt = ChatGPT()

    def generate_documentation(self, codebase):
        prompt = f"Generate documentation for the following codebase: {codebase}"
        response = self.gpt.chat_with_ollama(prompt)
        return response

    def execute(self, input_data):
        documentation = self.generate_documentation(input_data)
        self.save_to_file('documentation.md', documentation)

