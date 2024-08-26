from chat.chat_with_ollama import ChatGPT
from agents.base_agent import Agent
import os

class DocumentationGenerationAgent(Agent):
    def __init__(self, name):
        super().__init__(name)
        self.gpt = ChatGPT()

    def generate_documentation(self, prompt):
        response = self.gpt.chat_with_ollama(self.name, prompt)
        return response

    def generate_documentation_from_code(self, code):
        prompt = f"Generate documentation for the following code: {code}"
        response = self.gpt.chat_with_ollama(prompt)
        return response

    def execute(self, input_data):
        generated_docs = self.generate_documentation(input_data)
        self.save_to_file('generated_docs.md', generated_docs)

    def generate_readme_and_docs(self, directory):
        """
        Generate README and documentation files based on the prompt.

        This method creates a README.md and DOCUMENTATION.md file in the specified directory,
        containing an overview and initial documentation based on the prompt.
        """
        readme_content = (
            f"# Project Overview\n\n{self.prompt}\n\n## Directory Structure\nTBD\n"
        )
        documentation_content = "# Documentation\n\n## Overview\nDetailed documentation will be provided here as the project structure evolves.\n"

        readme_path = os.path.join(directory, "README.md")
        documentation_path = os.path.join(directory, "DOCUMENTATION.md")

        self.write_docs_to_directory(readme_path, readme_content)
        self.write_docs_to_directory(documentation_path, documentation_content)

        print(f"README.md and DOCUMENTATION.md created in {directory}")

    def write_docs_to_directory(self, path, content):
        """
        Write content to a specified file.

        Args:
            path (str): The path to the file.
            content (str): The content to write to the file.
        """
        with open(path, "w") as f:
            f.write(content)
