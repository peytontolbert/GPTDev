# agents/performance_evaluation_agent.py

from agents.base_agent import Agent
import json
from typing import List, Dict, Any
class PerformanceEvaluationAgent(Agent):
    def __init__(self, name, prompt):
        super().__init__(name, prompt)
        self.prompt = prompt

    def execute(self, input_data):
        prompt = self.generate_prompt(input_data)
        performance_score = float(self.gpt.chat_with_ollama(prompt, self.prompt))
        return performance_score

    def generate_prompt(self, input_data):
        agent_name = input_data['agent_name']
        result = input_data['result']
        # Implement the prompt generation logic here
        return (
            f"Evaluate the performance of the following agent:\n{agent_name}\n\n"
            f"Based on its output:\n{result}\n\n"
            "Provide a performance score between 0 and 1, where 1 represents perfect performance. "
            "Consider criteria such as correctness, efficiency, adherence to requirements, and overall quality."
        )

    def parse_response(self, response):
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {"raw_response": response}


