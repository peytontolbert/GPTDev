# agents/performance_evaluation_agent.py

from agents.base_agent import Agent
import json
from typing import List, Dict, Any
class PerformanceEvaluationAgent(Agent):
    def __init__(self, name, prompt):
        super().__init__(name)
        self.prompt = prompt

    def execute(self, input_data):
        prompt = self.generate_prompt(input_data)
        print(f"prompt: {prompt}")
        results = self.gpt.chat_with_ollama(prompt, self.prompt)
        performance_score = json.loads(results)
        score = performance_score['performance_score']
        return float(score)

    def generate_prompt(self, input_data):
        agent_name = input_data['agent_name']
        original_input = input_data['original_input']
        result = input_data['result']
        # Implement the prompt generation logic here

        return (
            f"Evaluate the performance of the following agent:\n{agent_name}\n\n"
            f"Original input provided to the agent:\n{original_input}\n\n"
            f"Output produced by the agent:\n{result}\n\n"
            "Evaluate the agent's performance on a scale from 0 to 1 based on the following criteria:\n"
            "1. Correctness: Does the output accurately reflect the input requirements?\n"
            "2. Efficiency: Was the output generated in an optimal manner?\n"
            "3. Adherence to Requirements: Did the output meet all the specified requirements?\n"
            "4. Overall Quality: How would you rate the overall quality of the output?\n\n"
            "Please provide an overall performance score, where 1 represents perfect performance. RESPOND WITH: {'performance_score': 0-1}"
        )
    def parse_response(self, response):
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {"raw_response": response}


