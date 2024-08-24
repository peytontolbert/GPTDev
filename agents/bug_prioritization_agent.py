from base_agent import Agent
from chat.chat_with_ollama import ChatGPT

class BugPrioritizationAgent(Agent):
    def __init__(self, name):
        super().__init__(name)
        self.gpt = ChatGPT()

    def prioritize_bugs(self, bugs):
        prompt = f"Prioritize the following bugs: {bugs}"
        response = self.gpt.chat_with_ollama(prompt)
        return response

    def execute(self, input_data):
        prioritized_bugs = self.prioritize_bugs(input_data)
        self.save_to_file('prioritized_bugs.txt', prioritized_bugs)

