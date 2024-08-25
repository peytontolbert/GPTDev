from agents.base_agent import Agent
import json

class KnowledgeRetrievalAgent(Agent):
    def __init__(self, name):
        super().__init__(name)

    def execute(self, input_data):
        prompt = self.generate_prompt(input_data)
        detailed_prompt = self.clarify_prompt(prompt)
        response = self.gpt.chat_with_ollama(detailed_prompt, self.name)
        return self.parse_response(response)

    def generate_prompt(self, input_data):
        return (
            f"Given the following task or code:\n{input_data}\n\n"
            "Search external knowledge sources (e.g., GitHub repositories, Stack Overflow, documentation databases) "
            "to find relevant information, code snippets, or best practices that can be used to improve the task. "
            "Summarize the findings in a JSON object with 'source' and 'content' as keys."
        )