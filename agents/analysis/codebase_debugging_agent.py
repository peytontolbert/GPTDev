from chat.chat_with_ollama import ChatGPT
from agents.base_agent import Agent
import os
import json
import pandas as pd
from glob import glob
from utils.token_utils import num_tokens_from_string
from agents.testing.unit_test_generation_agent import UnitTestGenerationAgent
from agents.analysis.function_extraction_agent import FunctionExtractionAgent
from agents.analysis.code_embedding_agent import CodeEmbeddingAgent
from agents.analysis.debugging_execution_agent import DebuggingExecutionAgent

class DebuggingAgent(Agent):
    """
    An agent that performs debugging on generated code.

    Attributes:
        gpt (ChatGPT): Instance of the ChatGPT class for communication.
        directory (str): Directory containing the code files.
        unit_test_agent (UnitTestGenerationAgent): Agent for generating unit tests.
        function_extraction_agent (FunctionExtractionAgent): Agent for extracting functions from code files.
        code_embedding_agent (CodeEmbeddingAgent): Agent for generating code embeddings.
        debugging_execution_agent (DebuggingExecutionAgent): Agent for executing debugging tasks.
    """

    def __init__(self, name, directory):
        """
        Initializes the DebuggingAgent with a name and directory.

        Args:
            name (str): The name of the agent.
            directory (str): The directory containing the code files.
        """
        super().__init__(name)
        self.gpt = ChatGPT()
        self.directory = directory
        self.unit_test_agent = UnitTestGenerationAgent('UnitTestGenerationAgent')
        self.function_extraction_agent = FunctionExtractionAgent('FunctionExtractionAgent', directory)
        self.code_embedding_agent = CodeEmbeddingAgent('CodeEmbeddingAgent')
        self.debugging_execution_agent = DebuggingExecutionAgent('DebuggingExecutionAgent')

    def execute(self, input_data):
        """
        Executes the debugging process on the generated code.

        Args:
            input_data (str): The input data for debugging.
        """
        self.debug_generated_code(input_data)

    def generate_prompt(self, input_data):
        """
        Generates a prompt from the input data.

        Args:
            input_data (str): The input data to generate the prompt from.
        """
        raise NotImplementedError("Each agent must implement the generate_prompt method.")

    def debug_generated_code(self, input_data):
        """
        Debugs the generated code by extracting functions, generating unit tests, and executing debugging tasks.

        Args:
            input_data (str): The input data for debugging.
        """
        extensions = ["py", "html", "js", "css", "c", "rs"]
        while True:
            code_files = []
            debug_logs = []
            failure_count = {}  # Keeps track of the number of failures for each function

            for extension in extensions:
                code_files.extend(
                    y
                    for x in os.walk(self.directory)
                    for y in glob(os.path.join(x[0], f"*.{extension}"))
                )
            self.log(f"Total number of files: {len(code_files)}")
            if len(code_files) == 0:
                self.log(
                    "Double check that you have downloaded the repo and set the code_dir variable correctly."
                )
            all_funcs = []
            unit_tests = []
            for code_file in code_files:
                funcs = self.function_extraction_agent.extract_functions(code_file)
                for func in funcs:
                    all_funcs.append(func)
                code_tokens_string = json.dumps(code_file)
                code_tokens = num_tokens_from_string(code_tokens_string)
                if code_tokens < 50000:
                    unit_test = self.unit_test_agent.generate_unit_tests(code_file)
                else:
                    for func in funcs:
                        unit_test = self.unit_test_agent.generate_unit_tests(func)
                        unit_tests.append(unit_test)
            if isinstance(all_funcs, dict):
                all_funcs = json.dumps(all_funcs)
            self.log(f"Total number of functions: {len(all_funcs)}")
            df = pd.DataFrame(all_funcs)
            df["code_embedding"] = df["code"].apply(
                lambda x: self.code_embedding_agent.get_embedding(x)
            )
            df["filepath"] = df["filepath"].apply(lambda x: x.replace(self.directory, ""))
            df.to_csv("functions.csv", index=True)
            df.head()
            debug_code_agent = self.debugging_execution_agent.debug_code(all_funcs)

            if not debug_code_agent or debug_code_agent.strip().lower() == "no":
                break
            else:
                self.log(debug_code_agent)



