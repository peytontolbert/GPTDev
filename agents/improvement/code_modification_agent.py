from agents.base_agent import Agent
"""
Code Modification Agent: Modifies a given code content based on user prompt
"""
class CodeModificationAgent(Agent):
    def __init__(self):
        super().__init__()

    def perform_task(self, input_data):
        prompt = self.generate_edit(input_data)
        response = self.generate_prompt(prompt)
        return response

    def generate_prompt(self, content: str, prompt) -> str:
        """
        Generate the edited content based on the prompt using the OpenAI API.

        Args:
            content (str): The original content of the file.

        Returns:
            str: The edited content generated by the OpenAI API.
        """
        prompt = f"{prompt}\n\n{content}"
        return prompt

    def generate_edit(self, input_data):
        """
        Not really useful for this
        """
        system_prompt = "Generate the edited content based on the prompt provided"
        response = self.gpt.chat_with_ollama(system_prompt, input_data)
        return response