# Import necessary modules
import os
import json
from utils.file_utils import get_file_paths, get_file_content, write_file
from chat.chat_with_ollama import ChatGPT

class CodeModularizationAgent:
    def __init__(self, directory, openai_api_key):
        self.directory = directory
        self.chat_gpt = ChatGPT()

    def traverse_and_modularize(self):
        file_paths = get_file_paths(self.directory, extensions=[".py"])
        for path in file_paths:
            self.modularize_file(path)

    def modularize_file(self, file_path):
        content = get_file_content(file_path)
        functions = self.extract_functions(content)
        base_dir = os.path.dirname(file_path)
        for func_name, func_code in functions.items():
            module_path = os.path.join(base_dir, f"{func_name}.py")
            write_file(module_path, func_code)
        self.request_delete_permission(file_path)

    def extract_functions(self, content):
        system_prompt = "You are a code modularization assistant."
        user_prompt = f"Extract functions from the following code:\n{content}"
        response = self.chat_gpt.chat_with_ollama(system_prompt, user_prompt)
        functions = json.loads(response["response"])
        return functions

    def request_delete_permission(self, file_path):
        user_input = input(f"Do you want to delete the original file {file_path}? (yes/no): ")
        if user_input.lower() == 'yes':
            os.remove(file_path)

# Example usage
if __name__ == "__main__":
    directory = "/path/to/your/codebase"
    openai_api_key = "your_openai_api_key"
    agent = CodeModularizationAgent(directory, openai_api_key)
    agent.traverse_and_modularize()

