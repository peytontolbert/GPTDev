from agents.base_agent import Agent
from chat.chat_with_ollama import ChatGPT
import json
"""
Code Understanding Agent: An agent that has the knowledge of a Software Development GPT Agent to understand and explain a given piece of code.
"""
class CodeUnderstandingAgent(Agent):
    def __init__(self):
        super().__init__("Code Understanding Agent")
        self.gpt = ChatGPT()
    
    def generate_prompt(self, code):
        return f"As an AI specializing in code comprehension, examine the following code:\n{code}\nWhat is its purpose and core functionality?"

    def perform_task(self, code):
        prompt = self.generate_prompt(code)
        response = self.gpt.chat_with_ollama(prompt)
        return self.parse_response(response)
    
    def parse_response(self, response):
        # Assuming the response is a text output that needs to be structured
        # Here, you could parse the response, or if it's already in JSON format, convert it
        try:
            result = json.loads(response)
        except json.JSONDecodeError:
            result = {"raw_response": response}
        return result
