from chat.chat_with_ollama import ChatGPT
from base_agent import Agent
import json

class PromptClarificationAgent(Agent):
    def __init__(self, name):
        super().__init__(name)
        self.gpt = ChatGPT()

    def clarify_prompt(self, prompt):
        while True:
            clarifying_prompt = "Please clarify the following prompt:"
            clarifying_prompt += (
                "\n\n"
                "Is anything unclear? If yes, only answer in the form:\n"
                "{remaining unclear areas} remaining questions. \n"
                "{Next question}\n"
                'If everything is sufficiently clear, only answer \"no\".'
            )
            clarifying_questions = self.gpt.chat_with_ollama_nojson(
                clarifying_prompt, prompt
            )
            self.log(clarifying_questions)
            user_input = input('(answer in text, or \"q\" to move on)\n')
            prompt += user_input
            self.log(prompt)

            if not user_input or user_input.strip().lower() == "q":
                break
        return json.dumps(prompt)

