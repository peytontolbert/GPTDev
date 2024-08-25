from agents.base_agent import Agent
import json

class NaturalLanguageRequirementsAgent(Agent):
    def __init__(self, name):
        super().__init__(name)

    def execute(self, input_data):
        prompt = self.generate_prompt(input_data)
        response = self.gpt.chat_with_ollama(prompt, self.name)
        return json.loads(response)

    def generate_prompt(self, input_data):
        decomposed_tasks = self.task_decomposition_agent.execute(input_data)  # Decompose tasks
        return (
            f"Given the following decomposed tasks:\n{json.dumps(decomposed_tasks, indent=2)}\n\n"
            "Parse these tasks into a structured format with the following information:\n"
            "1. Main objectives\n"
            "2. Functional requirements\n"
            "3. Non-functional requirements\n"
            "4. Constraints\n"
            "5. Acceptance criteria\n"
            "Provide the output as a JSON object."
        )
    
