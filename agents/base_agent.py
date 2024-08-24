from chat.chat_with_ollama import ChatGPT
import json

class Agent:
    def __init__(self, name):
        self.name = name
        self.gpt = ChatGPT()

    def execute(self, input_data):
        raise NotImplementedError("Each agent must implement the execute method.")

    def generate_prompt(self, input_data):
        raise NotImplementedError("Each agent must implement the generate_prompt method.")

    def clarify_prompt(self, prompt):
        clarifying_prompt = (
            'Is anything unclear? If yes, only answer in the form:\n'
            '{remaining unclear areas} remaining questions. \n'
            '{Next question}\n'
            'If everything is sufficiently clear, only answer "no".'
        )
        clarifying_questions = self.gpt.chat_with_ollama(clarifying_prompt, prompt)
        if "no" in clarifying_questions.lower():
            return prompt
        return prompt + clarifying_questions + "\n"

    def parse_response(self, response):
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {"raw_response": response}

    def log(self, message):
        print(f"[{self.name}] {message}")

    def save_to_file(self, filename, content):
        with open(filename, 'w') as file:
            file.write(content)
        self.log(f"Content saved to {filename}")

