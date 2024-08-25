from agents.base_agent import Agent
from chat.chat_with_ollama import ChatGPT

class BugIdentificationAgent(Agent):
    def __init__(self, name):
        super().__init__(name)
        self.gpt = ChatGPT()

    def identify_bugs(self, code):
        prompt = f"Identify bugs in the following code: {code}"
        response = self.gpt.chat_with_ollama(prompt)
        return response

    def execute(self, input_data):
        bugs = self.identify_bugs(input_data)
        self.save_to_file('identified_bugs.txt', bugs)

