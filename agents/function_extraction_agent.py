from base_agent import Agent
from src.codesearch import get_functions
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
            funcs = list(get_functions(code_file))
            for func in funcs:
                all_funcs.append(func)
        return all_funcs

    def execute(self, input_data):
        functions = self.extract_functions()
        self.save_to_file('extracted_functions.json', functions)

