from agents.base_agent import Agent
from chat.chat_with_ollama import ChatGPT

class BugFixingAgent(Agent):
    def __init__(self, name):
        super().__init__(name)
        self.gpt = ChatGPT()

    def fix_bugs(self, code, bugs):
        prompt = f"Fix the following bugs in the code: {bugs}\nCode: {code}"
        response = self.gpt.chat_with_ollama(prompt)
        return response

    def execute(self, input_data):
        code = input_data.get('code')
        bugs = input_data.get('bugs')
        fixed_code = self.fix_bugs(code, bugs)
        self.save_to_file('fixed_code.py', fixed_code)
    
