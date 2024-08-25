from agents.base_agent import Agent
from chat.chat_with_ollama import ChatGPT

class CodeAnalysisAgent(Agent):
    def __init__(self, name):
        super().__init__(name)
        self.gpt = ChatGPT()

    def analyze_code(self, code):
        prompt = f"Analyze the following code and identify any issues: {code}"
        response = self.gpt.chat_with_ollama(prompt)
        return response

    def execute(self, input_data):
        analysis_result = self.analyze_code(input_data)
        self.save_to_file('analysis_result.txt', analysis_result)

    def generate_prompt(self, input_data):
        raise NotImplementedError("Each agent must implement the generate_prompt method.")
