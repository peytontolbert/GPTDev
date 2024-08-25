# agents/agent_improvement_agent.py

from agents.base_agent import Agent
import json

class AgentImprovementAgent(Agent):
    def __init__(self, name):
        super().__init__(name)

    def execute(self, input_data):
        agent_name = input_data['agent_name']
        agent_code =input_data['agent_code']
        system_prompt = self.generate_prompt()
        improvement_prompt = (
            f"The following agent has underperformed:\n{agent_name}\n\n"
            f"Current implementation:\n{agent_code}\n\n"
            "Suggest improvements to enhance its performance."
        )
        improved_code = self.gpt.chat_with_ollama(system_prompt, improvement_prompt)
        return improved_code

    def generate_prompt(self):
        return "You are an Autonomous Agent Improver. Respond in a structured JSON format"