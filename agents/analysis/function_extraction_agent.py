from agents.base_agent import Agent
from utils.code_utils import get_until_no_space, get_function_name
import os
from glob import glob

class FunctionExtractionAgent(Agent):
    def __init__(self, name, directory):
        super().__init__(name)
        self.directory = directory

    def extract_functions(self):
        extensions = ["py", "html", "js", "css", "c", "rs"]
        code_files = []
        for extension in extensions:
            code_files.extend(
                y
                for x in os.walk(self.directory)
                for y in glob(os.path.join(x[0], f"*.{extension}"))
            )
        all_funcs = []
        for code_file in code_files:
            funcs = list(self.get_functions(code_file))
            for func in funcs:
                all_funcs.append(func)
        return all_funcs

    def execute(self, input_data):
        functions = self.extract_functions()
        self.save_to_file('extracted_functions.json', functions)


    def get_functions(self, filepath):
        """
        Get all functions in a Python file.
        """
        with open(filepath, 'r') as file:
            whole_code = file.read().replace('\r', '\n')
        all_lines = whole_code.split("\n")
        for i, l in enumerate(all_lines):
            if l.startswith("def "):
                code = get_until_no_space(all_lines, i)
                function_name = get_function_name(code)
                yield {"code": code, "function_name": function_name, "filepath": filepath}
