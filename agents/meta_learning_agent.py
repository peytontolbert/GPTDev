from agents.base_agent import Agent
import json
from typing import Dict, Any
class MetaLearningAgent(Agent):
    def __init__(self, name):
        super().__init__(name)

    def execute(self, input_data):
        prompt = self.generate_prompt(input_data)
        detailed_prompt = self.clarify_prompt(prompt)
        response = self.gpt.chat_with_ollama(detailed_prompt, self.name)
        return self.parse_response(response)

    def generate_prompt(self, input_data):
        return (
            f"Analyze the following past iterations and their outcomes:\n{input_data}\n\n"
            "Identify patterns that led to success and failures. Suggest strategies or adjustments that can be implemented in future tasks "
            "to enhance the effectiveness of the system. Provide the suggestions in a structured format."
        )

    def adjust_improvement_strategies(self, meta_analysis: Dict[str, Any]) -> None:
        for agent_name, adjustments in meta_analysis.items():
            if agent_name in self.agent_details:
                self.agent_details[agent_name]["improvement_strategy"] = adjustments["new_strategy"]
                self.log(f"Adjusted improvement strategy for {agent_name} based on meta-learning feedback.")