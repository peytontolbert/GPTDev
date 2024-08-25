from agents.base_agent import Agent
"""
Code Review Agent: Reviews a inputted code to give a solid response for a Software Engineering GPT Agent.
"""
class CodeReviewAgent(Agent):
    def __init__(self):
        super().__init__()

    def perform_task(self, input_data):
        review = self.generate_prompt(input_data)
        # Save the review to a file or database
        with open('code_review.txt', 'w') as f:
            f.write(review)

    def generate_prompt(self, input_data):
        prompt = f"Review the following code: {input_data}"
        response = self.gpt.chat_with_ollama(prompt)
        return response

