# Import necessary modules
import os
import json
from utils.file_utils import write_file, get_file_content, get_file_paths
from chat.chat_with_ollama import ChatGPT


class DocumentationAgent:
    def __init__(self, directory):
        self.directory = directory
        self.gpt = ChatGPT()

    def generate_readme(self):
        readme_content = (
            f"# Project Overview\n\n"
            f"## Directory Structure\n"
            f"{self.get_directory_structure()}\n"
        )
        readme_path = os.path.join(self.directory, "README.md")
        self.write_docs_to_directory(readme_path, readme_content)
        print(f"README.md created in {self.directory}")

    def generate_documentation(self):
        documentation_content = (
            "# Documentation\n\n"
            "## Overview\n"
            "Detailed documentation will be provided here as the project structure evolves.\n"
        )
        documentation_path = os.path.join(self.directory, "DOCUMENTATION.md")
        self.write_docs_to_directory(documentation_path, documentation_content)
        print(f"DOCUMENTATION.md created in {self.directory}")

    def get_directory_structure(self):
        file_paths = get_file_paths(self.directory, extensions=[".py", ".md", ".txt"])
        structure = ""
        for path in file_paths:
            structure += f"{path}\n"
        return structure

    def write_docs_to_directory(self, path, content):
        write_file(path, content)

    def update_readme(self, program_structure):
        systemprompt = f"""Given the following program structure in JSON format:

        ```json
        {json.dumps(program_structure, indent=2)}
        ```

        Please provide a concise summary of the program's architecture, including the purpose of each module, class, and their relationships.
        """
        structure_summary_response = self.gpt.chat_with_ollama(
            systemprompt, json.dumps(program_structure, indent=2)
        )

        readme_path = os.path.join(self.directory, "README.md")
        structure_content = f"\n## Program Structure\n{structure_summary_response}\n"

        with open(readme_path, "a") as f:
            f.write(structure_content)
        print(f"Program structure summary added to {readme_path}")

    def update_documentation(self, shared_dependencies, filepaths):
        dependencies_prompt = f"""Given the following shared dependencies and filepaths in JSON format:

        ```json
        {json.dumps(shared_dependencies, indent=2)}
        ```

        Please provide a detailed explanation of the shared dependencies, their purpose, and how they interact with each other.
        """
        dependencies_summary_response = self.gpt.chat_with_ollama(
            dependencies_prompt, json.dumps(shared_dependencies, indent=2)
        )

        documentation_path = os.path.join(self.directory, "DOCUMENTATION.md")
        dependencies_content = f"\n## Shared Dependencies\n{dependencies_summary_response}\n"

        with open(documentation_path, "a") as f:
            f.write(dependencies_content)
        print(f"Shared dependencies details added to {documentation_path}")

