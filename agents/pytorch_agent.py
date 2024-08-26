from base_agent import Agent
import os

class PyTorchAgent(Agent):
    def __init__(self, name, documentation_path):
        super().__init__(name)
        self.documentation_path = documentation_path

    def execute(self, input_data):
        self.log(f"Searching for: {input_data}")
        results = self.search_documentation(input_data)
        return results

    def generate_prompt(self, input_data):
        return f"Find information about {input_data} in the PyTorch documentation."

    def search_documentation(self, query):
        results = []
        for root, dirs, files in os.walk(self.documentation_path):
            for file in files:
                if file.endswith(".html") or file.endswith(".md"):
                    with open(os.path.join(root, file), 'r') as f:
                        content = f.read()
                        if query.lower() in content.lower():
                            results.append((file, content))
        return results

    def parse_response(self, response):
        return response

