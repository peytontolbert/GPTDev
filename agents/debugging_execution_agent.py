from agents.base_agent import Agent
from chat.chat_with_ollama import ChatGPT

class DebuggingExecutionAgent(Agent):
    def __init__(self, name):
        super().__init__(name)
        self.gpt = ChatGPT()

    def execute_debugging(self, code):
        prompt = f"Debug the following code: {code}"
        response = self.gpt.chat_with_ollama(prompt)
        return response

    def execute(self, input_data):
        debugging_result = self.execute_debugging(input_data)
        self.save_to_file('debugging_result.txt', debugging_result)

