from agents.base_agent import Agent
"""
Code Generation Agent: Generates specific code based on a prompt.
"""
class CodeGenerationAgent(Agent):
    def __init__(self, name):
        super().__init__(name)

    def execute(self, input_data):
        generated_code = self.generate_prompt(input_data)
        # Save the generated code to a file or database
        with open('generated_code.py', 'w') as f:
            f.write(generated_code)

    def generate_prompt(self, input_data):
        prompt = f"Generate code for the following requirements: {input_data}"
        response = self.gpt.chat_with_ollama(self.name, prompt)
        return response

