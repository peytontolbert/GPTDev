from agents.base_agent import Agent
"""
Code Review Agent: Reviews a inputted code to give a solid response for a Software Engineering GPT Agent.

Classes:
    CodeReviewAgent: An agent that reviews code and generates a response.

"""
class CodeReviewAgent(Agent):
    """
    An agent that reviews code and generates a response.
    """
    def __init__(self):
        """
        Initializes the CodeReviewAgent.
        """
        super().__init__()

    def perform_task(self, input_data):
        """
        Performs the task of reviewing the input code.

        Args:
            input_data (str): The code to be reviewed.
        """
        review = self.generate_prompt(input_data)
        # Save the review to a file or database
        with open('code_review.txt', 'w') as f:
            f.write(review)

    def generate_prompt(self, input_data):
        """
        Generates a prompt for reviewing the input code.

        Args:
            input_data (str): The code to be reviewed.

        Returns:
            str: The response from the GPT model.
        """
        prompt = f"Review the following code: {input_data}"
        response = self.gpt.chat_with_ollama(prompt)
        return response



