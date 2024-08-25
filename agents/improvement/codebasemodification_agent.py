import os
import openai
import json
from typing import List, Dict, Any
from chat.chat_with_ollama import ChatGPT
from dotenv import load_dotenv
from utils.file_utils import get_file_content, write_file, get_file_paths
import shutil
import tempfile
from agents.communication.prompt_clarification_agent import PromptClarificationAgent
from agents.documentation.documentation_generation_agent import DocumentationGenerationAgent
from agents.integration.code_integration_agent import CodeIntegrationAgent
from agents.improvement.code_modification_agent import CodeModificationAgent
from agents.testing.testing_agent import TestingAgent
from agents.base_agent import Agent
# Load environmental variables and set global constants
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

"""
Codebase Modification Agent: Correctly modifies a codebase given a specific prompt.
"""
class CodebaseModificationAgent(Agent):
    def __init__(self, prompt: str, directory: str, model: str = "gpt-4-1106-preview"):
        """
        Initialize the EditCodebaseAgent with the given prompt, directory, and model.

        Args:
            prompt (str): The user prompt for editing the codebase.
            directory (str): The directory of the codebase to be edited.
            model (str): The model to be used for generating edits. Default is "gpt-4-1106-preview".
        """
        super().__init__()
        self.prompt = prompt
        self.directory = directory
        self.gpt = ChatGPT()
        self.prompt_clarification_agent = PromptClarificationAgent()
        self.documentation_generation_agent = DocumentationGenerationAgent()
        self.code_modification_agent = CodeModificationAgent()
        self.code_integration_agent = CodeIntegrationAgent()
        self.testing_agent = TestingAgent()

    def perform_task(self, input_data):
        self.prompt = self.prompt_clarification_agent.clarify_prompt(self.prompt)
        self.documentation_generation_agent.generate_readme_and_docs(self.prompt, self.directory)
        self.edit_codebase()
        self.testing_agent.run_tests(self.directory)

    def generate_prompt(self, input_data):
        return f"Modify the codebase in the directory {self.directory} based on the following prompt: {self.prompt}"

    def edit_and_test_codebase(self):
        """
        Edit the codebase in a temporary directory and run tests.

        This method creates a temporary directory, copies the original files into it,
        generates edits for each file, runs tests on the modified files, and replaces
        the original files with the modified files if the tests pass.
        """
        temp_dir = self.create_temp_directory()
        file_paths = get_file_paths(temp_dir)

        for file_path in file_paths:
            content = get_file_content(file_path)
            edited_content = self.code_modification_agent.generate_edit(content)
            write_file(file_path, edited_content)

        # Run tests in the temporary directory
        result = os.system(f"pytest {temp_dir}")

        if result == 0:
            # Tests passed, replace original files with modified files
            for file_path in file_paths:
                original_file_path = os.path.join(
                    self.directory, os.path.relpath(file_path, temp_dir)
                )
                shutil.copy(file_path, original_file_path)
            print("Codebase successfully edited and tested.")
        else:
            print("Tests failed. Original codebase remains unchanged.")

    # ... (other methods)

    def create_temp_directory(self):
        """
        Create a temporary directory and copy the original files into it.

        Returns:
            str: The path to the temporary directory.
        """
        temp_dir = tempfile.mkdtemp()
        for file_path in get_file_paths(self.directory):
            shutil.copy(file_path, temp_dir)
        return temp_dir

    def clarify_prompt(self):
        """
        Clarify the prompt by asking the user for additional information if needed.

        This method interacts with the user to ensure that the prompt is clear and complete.
        It appends user responses to the prompt until the user indicates that no further clarification is needed.

        Returns:
            str: The clarified prompt in JSON format.
        """
        while True:
            clarifying_prompt = (
                "Is anything unclear? If yes, only answer in the form:\n"
                "{remaining unclear areas} remaining questions. \n"
                "{Next question}\n"
                "If everything is sufficiently clear, only answer 'no'."
            )
            response = openai.Completion.create(
                model=self.model,
                prompt=f"{clarifying_prompt}\n\n{self.prompt}",
                max_tokens=150,
            )
            clarifying_questions = response.choices[0].text.strip()
            print(clarifying_questions)
            user_input = input('(answer in text, or "q" to move on)\n')
            self.prompt += user_input
            print()

            if not user_input or user_input.strip().lower() == "q":
                break
        return json.dumps(self.prompt)

    def parse_response(self, response):
        """
        Parse the response from the OpenAI API.

        Args:
            response (str | dict | list): The response from the OpenAI API.

        Returns:
            dict | list | None: The parsed response, or None if parsing fails.
        """
        if response and isinstance(response, str):
            try:
                return json.loads(response)
            except json.JSONDecodeError:
                print("Failed to decode JSON. Handling as a string or other format.")
                return None
        elif isinstance(response, (dict, list)):
            return response
        else:
            print("Unexpected data type received.")
            return None

    def edit_codebase(self):
        """
        Edit the codebase based on the prompt.

        This method retrieves all file paths in the specified directory, generates edits for each file,
        and writes the edited content back to the files.
        """
        file_paths = get_file_paths(self.directory)

        for file_path in file_paths:
            content = get_file_content(file_path)
            edited_content = self.code_modification_agent.perform_task(content, self.prompt)
            write_file(file_path, edited_content)


    def find_relevant_portions(self, content: str) -> List[str]:
        """
        Find relevant portions of the code to be modified based on the prompt.

        Args:
            content (str): The original content of the file.

        Returns:
            List[str]: A list of relevant portions of the code to be modified.
        """
        response = self.gpt.chat_with_ollama(system_prompt, prompt)
        return response.choices[0].text.strip().split("\n")

    def test_integrations(self):
        """
        Run tests to ensure the changes do not break the codebase.

        This method runs the test suite using pytest to verify that the changes made to the codebase
        do not introduce any new issues or break existing functionality.
        """
        os.system("pytest")



