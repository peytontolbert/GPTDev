from agents.base_agent import Agent
"""
Code Style Enforcement Agent: Ensures that the code adheres to predefined style guidelines.
"""
class CodeStyleEnforcementAgent(Agent):
    def __init__(self):
        super().__init__()

    def perform_task(self, input_data):
        style_report = self.generate_prompt(input_data)
        # Save the style report to a file or database
        with open('style_report.txt', 'w') as f:
            f.write(style_report)

    def generate_prompt(self, input_data):
        prompt = f"Enforce code style guidelines on the following code: {input_data}"
        response = self.gpt.chat_with_ollama(prompt)
        return response

