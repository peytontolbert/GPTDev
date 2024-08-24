from base_agent import Agent
"""
Code Documentation Agent: Traverse and documents an entire codebase.
"""
class CodeDocumentationAgent(Agent):
    def __init__(self):
        super().__init__()

    def perform_task(self, input_data):
        documentation = self.generate_prompt(input_data)
        # Save the documentation to a file or database
        with open('documentation.md', 'w') as f:
            f.write(documentation)

    def generate_prompt(self, input_data):
        prompt = f"Generate documentation for the following codebase: {input_data}"
        response = self.gpt.chat_with_ollama(prompt)
        return response

