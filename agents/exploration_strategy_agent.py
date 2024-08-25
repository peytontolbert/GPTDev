from agents.base_agent import Agent
import json

class ExplorationStrategyAgent(Agent):
    def __init__(self, name):
        super().__init__(name)

    def execute(self, input_data):
        prompt = self.generate_prompt(input_data)
        detailed_prompt = self.clarify_prompt(prompt)
        response = self.gpt.chat_with_ollama(detailed_prompt, self.name)
        return self.parse_response(response)

    def generate_prompt(self, input_data):
        return (
            f"Given the following problem or task:\n{input_data}\n\n"
            "Explore multiple strategies or solutions that could address this problem. "
            "Ensure that each strategy is different in its approach, considering various angles such as performance, security, and scalability. "
            "Present the strategies in a structured format with pros and cons for each."
        )
