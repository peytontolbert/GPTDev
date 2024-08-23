# Import necessary modules
import os
import json
from utils.file_utils import write_file, get_file_content, get_file_paths
from chat.chat_with_ollama import ChatGPT


class TestUnitAgent:
    def __init__(self, directory):
        self.directory = directory
        self.gpt = ChatGPT()

    def generate_tests(self):
        file_paths = get_file_paths(self.directory, extensions=[".py"])
        for path in file_paths:
            file_content = get_file_content(path)
            test_cases = self.create_test_cases(file_content)
            test_file_path = self.get_test_file_path(path)
            self.write_tests_to_directory(test_file_path, test_cases)
            print(f"Test cases created for {path} and saved to {test_file_path}")

    def create_test_cases(self, code):
        system_prompt = (
            "As an AI adept in testing code, create appropriate test cases for the following code. "
            "Compile the results of your tests into a Python dictionary."
        )
        test_cases_response = self.gpt.chat_with_ollama(system_prompt, code)
        return test_cases_response

    def get_test_file_path(self, original_file_path):
        directory, filename = os.path.split(original_file_path)
        test_filename = f"test_{filename}"
        test_directory = os.path.join(directory, "tests")
        if not os.path.exists(test_directory):
            os.makedirs(test_directory)
        return os.path.join(test_directory, test_filename)

    def write_tests_to_directory(self, path, content):
        write_file(path, content)

    def run_tests(self):
        test_files = get_file_paths(self.directory, extensions=[".py"], subdirectory="tests")
        for test_file in test_files:
            os.system(f"pytest {test_file}")
            print(f"Tests run for {test_file}")
