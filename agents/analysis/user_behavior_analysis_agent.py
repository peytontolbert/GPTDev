from agents.base_agent import Agent
import json

class UserBehaviorAnalysisAgent(Agent):
    def __init__(self, name="UserBehaviorAnalysisAgent"):
        super().__init__(name)

    def perform_task(self, input_data):
        """
        Analyzes user behavior data to extract insights and provide recommendations for software improvement.
        :param input_data: A dictionary containing user interaction logs, usage statistics, and feedback.
        :return: A dictionary with identified behavior patterns, potential issues, and improvement suggestions.
        """
        prompt = self.generate_prompt(input_data)
        response = self.gpt.chat_with_ollama(prompt)
        return self.parse_response(response)

    def generate_prompt(self, input_data):
        """
        Generates a prompt for the GPT model to analyze user behavior data.
        :param input_data: A dictionary containing user interaction logs, usage statistics, and feedback.
        :return: A string prompt that instructs the model to analyze the data.
        """
        return (
            f"Given the following user behavior data:\n{json.dumps(input_data, indent=2)}\n\n"
            "Analyze the data and identify any patterns or recurring issues that might impact user experience. "
            "Provide insights on how the software can be improved to better meet user needs and preferences. "
            "Include any recommendations for features or changes that could enhance user engagement and satisfaction."
        )

    def parse_response(self, response):
        """
        Parses the GPT model's response into a structured format.
        :param response: The raw response from the GPT model.
        :return: A dictionary containing the analysis results.
        """
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {"raw_response": response}