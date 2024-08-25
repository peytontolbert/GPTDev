# agents/deployment_agent.py

from agents.base_agent import Agent
from chat.chat_with_ollama import ChatGPT

class OllamaChatAgent(Agent):
    def __init__(self, name, directory):
        super().__init__(name)
        self.gpt = ChatGPT()

    def execute(self, input_data):
        system_prompt = input_data['system_prompt']
        prompt = input_data['prompt']
        results = self.gpt.chat_with_ollama(system_prompt, prompt)
        return results