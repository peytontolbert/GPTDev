# Import necessary modules
import openai
import os
import sys
import time
import json
import re
import ast
from chat.chat_with_ollama import ChatGPT
from utils.constants import DEFAULT_DIRECTORY, DEFAULT_MODEL, DEFAULT_MAX_TOKENS
from agents.analysis.code_embedding_agent import CodeEmbeddingAgent
from agents.analysis.function_extraction_agent import FunctionExtractionAgent
from prompts.codingagents import (
    clarifying_agent,
    algorithm_agent,
    coding_agent,
    debug_agent,
    file_code_agent,
    unit_test_agent,
)
from utils.token_utils import num_tokens_from_string
from utils.file_utils import write_file, get_file_content, get_file_paths
from glob import glob
import pathlib
import pandas as pd
import numpy as np
import traceback
from dotenv import load_dotenv
from agents.base_agent import Agent
from agents.analysis.code_embedding_agent import CodeEmbeddingAgent
# Initialize OpenAI and GitHub API keys
openai.api_key = os.getenv("OPENAI_API_KEY")

tokenLimit = 50000
DEFAULT_MODEL = "gpt-4-1106-preview"  # Set your default model here
"""
Codebase Generation Agent: Generates an entire codebase from a prompt.
"""

# ---  GenerateCodebaseAgent class ---
class GenerateCodebaseAgent(Agent):
    def __init__(self, prompt, directory, model=DEFAULT_MODEL):
        self.prompt = prompt
        self.directory = directory
        self.functions = FunctionExtractionAgent()
        self.gpt = ChatGPT()
        self.embedding_agent = CodeEmbeddingAgent()

    def execute(self, input_data):
        # Implement the main logic here
        prompt = self.generate_prompt(input_data)
        self.generate_codebase(prompt)

    def generate_prompt(self, input_data):
        # Implement prompt generation logic here
        return f"Generate a prompt to generate a codebase based on the following user input: {input_data}"

    def clarify_prompt(self):
        while True:
            clarifying_prompt = clarifying_agent()
            clarifying_prompt += (
                "\n\n"
                "Is anything unclear? If yes, only answer in the form:\n"
                "{remaining unclear areas} remaining questions. \n"
                "{Next question}\n"
                'If everything is sufficiently clear, only answer "no".'
            )
            clarifying_questions = self.gpt.chat_with_ollama_nojson(
                clarifying_prompt, self.prompt
            )
            print(clarifying_questions)
            user_input = input('(answer in text, or "q" to move on)\n')
            self.prompt += user_input
            print()

            if not user_input or user_input.strip().lower() == "q":
                break
        return json.dumps(self.prompt)

    def parse_response(self, response):
        # Check if design_response is not empty and is a string
        if response and isinstance(response, str):
            try:
                # Attempt to parse the JSON string
                program_design = json.loads(response)
                return program_design
            except json.JSONDecodeError:
                # Handle the case where design_response is not a valid JSON string
                print("Failed to decode JSON. Handling as a string or other format.")
                # Here, you can implement custom logic depending on your needs
                # For example, check if it's a specific string format you can handle
                # Or log the error and return a default object or error message
                return None
        elif isinstance(response, (dict, list)):
            # If design_response is already a dictionary or list, return it directly
            return response
        else:
            # Handle other unexpected data types
            print("Unexpected data type received.")
            return None

    def generate_readme_and_docs(self):
        readme_content = (
            f"# Project Overview\n\n{self.prompt}\n\n## Directory Structure\nTBD\n"
        )
        documentation_content = "# Documentation\n\n## Overview\nDetailed documentation will be provided here as the project structure evolves.\n"

        readme_path = os.path.join(self.directory, "README.md")
        documentation_path = os.path.join(self.directory, "DOCUMENTATION.md")

        self.write_docs_to_directory(readme_path, readme_content)
        self.write_docs_to_directory(documentation_path, documentation_content)

        print(f"README.md and DOCUMENTATION.md created in {self.directory}")

    def update_readme(self, program_structure):
        # Generate program structure summary using Ollama
        systemprompt = f"""Given the following program structure in JSON format:

        ```json
        {json.dumps(program_structure, indent=2)}
        ```

        Please provide a concise summary of the program's architecture, including the purpose of each module, class, and their relationships.
        """
        structure_summary_response = self.gpt.chat_with_ollama(
            systemprompt, json.dumps(program_structure, indent=2)
        )

        # Append the generated summary to the README
        readme_path = os.path.join(self.directory, "README.md")
        structure_content = f"\n## Program Structure\n{structure_summary_response}\n"

        with open(readme_path, "a") as f:
            f.write(structure_content)

    def update_documentation(self, shared_dependencies, filepaths):
        # Generate shared dependencies summary using Ollama
        systemprompt = f"""Given the following shared dependencies in JSON format:

        ```json
        {json.dumps(shared_dependencies, indent=2)}
        ```

        Please provide a concise summary of the shared dependencies, including their purpose and how they are used across different modules.
        """
        dependencies_summary_response = self.gpt.chat_with_ollama(
            systemprompt, json.dumps(shared_dependencies, indent=2)
        )

        # Append the generated summary to the DOCUMENTATION
        documentation_path = os.path.join(self.directory, "DOCUMENTATION.md")
        dependencies_content = f"\n## Shared Dependencies\n{dependencies_summary_response}\n"

        with open(documentation_path, "a") as f:
            f.write(dependencies_content)
        print(f"Shared dependencies summary added to {documentation_path}")

    def write_docs_to_directory(self, filepath, filecode):
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

        with open(filepath, "a") as f:
            f.write(str(filecode))

    def write_files_to_directory(self, filepath, filecode):
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

        # Normalize the file path
        file_path = os.path.normpath(os.path.join(self.directory, filepath))
        with open(file_path, "a") as f:
            f.write(filecode)

    def debug_generated_code(self):
        extensions = ["py", "html", "js", "css", "c", "rs"]
        while True:
            code_files = []
            debug_logs = []
            failure_count = (
                {}
            )  # Keeps track of the number of failures for each function

            for extension in extensions:
                code_files.extend(
                    y
                    for x in os.walk(self.directory)
                    for y in glob(os.path.join(x[0], f"*.{extension}"))
                )
            print("Total number of files:", len(code_files))
            if len(code_files) == 0:
                print(
                    "Double check that you have downloaded the repo and set the code_dir variable correctly."
                )
            all_funcs = []
            unit_tests = []
            for code_file in code_files:
                funcs = list(self.functions.get_functions(code_file))
                for func in funcs:
                    all_funcs.append(func)
                code_tokens_string = json.dumps(code_file)
                code_tokens = num_tokens_from_string(code_tokens_string)
                if code_tokens < tokenLimit:
                    unit_test = unit_test_agent(code_file)
                else:
                    for func in funcs:
                        unit_test_prompt = unit_test_agent()
                        unit_test = self.gpt.chat_with_ollama(unit_test_prompt, func)
                        unit_tests.append(unit_test)
            if isinstance(all_funcs, dict):
                all_funcs = json.dumps(all_funcs)
            print("Total number of functions:", len(all_funcs))
            df = pd.DataFrame(all_funcs)
            df["code_embedding"] = df["code"].apply(
                lambda x: self.embedding_agent.get_embedding(x, engine="text-embedding-ada-002")
            )
            df["filepath"] = df["filepath"].apply(lambda x: x.replace(self.directory, ""))
            df.to_csv("functions.csv", index=True)
            df.head()
            debug_code_agent = self.gpt.chat_with_ollama(debug_agent, all_funcs)

            if not debug_code_agent or debug_code_agent.strip().lower() == "no":
                break
            else:
                print(debug_code_agent)

    def filter_filepaths(self, filepaths):
        filepaths_list = ast.literal_eval(filepaths)
        return [fp.lstrip("/") for fp in filepaths_list]

    def generate_codebase(self, prompt):
        """Main orchestration method to generate the entire codebase."""

        self.new_prompt_string = self.clarify_prompt()
        print(self.new_prompt_string)

        self.generate_readme_and_docs()

        program_structure = self.design_program_structure()
        print("Program structure designed:", program_structure)

        self.update_readme(program_structure)

        initial_dependencies = self.generate_shared_dependencies(
            program_structure, self.prompt
        )

        filepaths = self.generate_file_paths(
            program_structure, initial_dependencies, self.prompt
        )
        print(filepaths)

    def generate_readme_and_docs(self):
        readme_content = f"# Project Overview\n\n{self.prompt}\n\n## Directory Structure\nTBD\n"
        documentation_content = "# Documentation\n\n## Overview\nDetailed documentation will be provided here as the project structure evolves.\n"
        
        readme_path = os.path.join(self.directory, "README.md")
        documentation_path = os.path.join(self.directory, "DOCUMENTATION.md")
        
        self.write_docs_to_directory(readme_path, readme_content)
        self.write_docs_to_directory(documentation_path, documentation_content)

        print(f"README.md and DOCUMENTATION.md created in {self.directory}")

            
    def update_readme(self, program_structure):
        # Generate program structure summary using Ollama
        systemprompt = f"""Given the following program structure in JSON format:

        ```json
        {json.dumps(program_structure, indent=2)}
        ```

        Please provide a concise summary of the program's architecture, including the purpose of each module, class, and their relationships.
        """
        structure_summary_response = self.gpt.chat_with_ollama(systemprompt, json.dumps(program_structure, indent=2))
        
        # Append the generated summary to the README
        readme_path = os.path.join(self.directory, "README.md")
        structure_content = f"\n## Program Structure\n{structure_summary_response}\n"
        
        with open(readme_path, "a") as f:
            f.write(structure_content)
        print(f"Program structure summary added to {readme_path}")


    def update_documentation(self, shared_dependencies, filepaths):
        # Generate shared dependencies details using Ollama
        dependencies_prompt = f"""Given the following shared dependencies and filepaths in JSON format:

        ```json
        {json.dumps(shared_dependencies, indent=2)}
        ```

        Please provide a detailed explanation of these dependencies, including their purpose and how they are used within the program.
        """
        dependencies_details_response = self.gpt.chat_with_ollama(dependencies_prompt, json.dumps(shared_dependencies, indent=2))
        
        # Generate file paths details using Ollama
        filepaths_prompt = f"""Given the following file paths in JSON format:

        ```json
        {json.dumps(filepaths, indent=2)}
        ```

        Please provide a detailed explanation of the contents and purpose of each file, and how they interact within the program.
        """
        filepaths_details_response = self.gpt.chat_with_ollama(filepaths_prompt, json.dumps(filepaths, indent=2))
        
        # Append the generated details to the DOCUMENTATION
        documentation_path = os.path.join(self.directory, "DOCUMENTATION.md")
        dependencies_content = f"\n## Shared Dependencies\n{dependencies_details_response}\n"
        filepaths_content = f"\n## Filepaths\n{filepaths_details_response}\n"
        
        with open(documentation_path, "a") as f:
            f.write(dependencies_content)
            f.write(filepaths_content)
        print(f"Shared dependencies and file paths details added to {documentation_path}")



    def update_readme_for_code(self, filecode):
        # Generate code summary using Ollama
        systemprompt = f"""Given the following code:

        ```python
        {filecode}
        ```

        Please provide a concise summary of what the code does, its main components, and its purpose. This will be placed in README.md.
        """
        code_summary_response = self.gpt.chat_with_ollama_nojson(systemprompt, filecode)
        
        # Append the generated summary to the README
        readme_path = os.path.join(self.directory, "README.md")
        code_summary = f"\n## Code Summary\n{code_summary_response}\n"
        
        with open(readme_path, "a") as f:
            f.write(code_summary)
        print(f"Code summary added to {readme_path}")


    def update_documentation_for_code(self, filecode):
        # Generate code implementation details using Ollama
        systemprompt = f"""Given the following code:

        ```python
        {filecode}
        ```

        Please provide a detailed explanation of the code's implementation, including key functions, logic flow, and any significant design decisions.
        """
        code_details_response = self.gpt.chat_with_ollama(systemprompt, filecode)
        
        # Append the generated details to the DOCUMENTATION
        documentation_path = os.path.join(self.directory, "DOCUMENTATION.md")
        code_details = f"\n## Code Implementation Details\n{code_details_response}\n"
        
        with open(documentation_path, "a") as f:
            f.write(code_details)
        print(f"Code details added to {documentation_path}")


    def design_program_structure(self):
        print("Designing program structure based on requirements...")

        systemprompt = f"""Based on the following clarified requirements:

        {self.prompt}


        Provide a JSON structure of the program architecture, including modules, classes, functions, 
        relationships, and dataflow. An example format is provided below:

        {{
            "modules": [],
            "classes": [],
            "functions": [],
            "relationships": [],
            "dataflow": []
        }}

        This description should include:

        - Module names and their responsibilities
        - Class definitions and their methods
        - Functions and their purpose
        - Relationships and interactions between components
        - Data flow within the program
        
        Present the design in a structured JSON format.
        """
        design_response = self.gpt.chat_with_ollama(systemprompt, self.prompt)
        print(f"program design:  {design_response}")
        # Parse the returned JSON string into a Python dictionary.
        program_design = self.parse_response(design_response)
        return program_design
    def generate_file_paths(self, program_structure, initial_dependencies, readme):
        # Convert program_structure to JSON string if not already in that form
        program_structure_json = json.dumps(program_structure) if isinstance(program_structure, dict) else program_structure
        systemprompt = f"""You are an AI developer who is trying to write generate a list of filepaths that will generate code for the user based on their intent.
        Based on the follow program requirements:
        {program_structure_json}
        {initial_dependencies}
        When given project overview, create a complete, exhaustive list of filepaths that the user would write to make the program.
        An example format is provided below:

                    
        [README.md, main.py, models.py, data.py, utils.py]
        
        The filepaths should only list the paths for the program files and folders, structured in a way that adheres to the design specified in the program architecture. Simply provide the array structure of filepaths, without any additional explanation.
        """
        result = self.gpt.chat_with_ollama_nojson(system_prompt = systemprompt, prompt = readme)
        print(f"file path: {result}")
        if isinstance(result, list):
            return result
        list_result = self.parse_filepath_list(result)
        return list_result

    def parse_filepath_list(self, result):    
        result = result.strip("` \n")
        result = result.strip("\n")
        # If it's a dictionary, extract the list under 'filepaths'
        if isinstance(result, dict):
            return result.get('filepaths', [])
        # Debugging: Print the exact string we're trying to parse
        print(f"Raw result after stripping: {repr(result)}")
            
        # Extract only the part of the string that represents the list
        list_start = result.find('[')
        list_end = result.find(']')
        
        if list_start != -1 and list_end != -1:
            list_str = result[list_start:list_end + 1]  # Extract the content within the square brackets
        else:
            print("Failed to locate list in the result.")
            return []
        
        # Remove any potential invisible characters within the list string
        list_str = re.sub(r'[^\x20-\x7E]', '', list_str)
        
        # Attempt to evaluate the list string as a Python list
        try:
            filepaths = ast.literal_eval(list_str)
            if isinstance(filepaths, list):
                return filepaths
        except (SyntaxError, ValueError):
            print("Literal eval failed, attempting further manual parsing.")
        
        # Fallback: Manual parsing by splitting the cleaned list string
        filepaths = [item.strip(" '\"") for item in list_str.strip("[]").split(",") if item.strip()]
        print(f"last filepaths: {filepaths}")
        return filepaths

        
        
    def generate_shared_dependencies(self, program_structure, readme):

        # Prepare the prompt for the AI developer based on the program structure and file paths
        systemprompt = f"""As an AI developer, understand the program's architecture and file structure to identify shared dependencies required across the codebase. The program structure and intended file paths are as follows:

        Program Structure: {json.dumps(program_structure, indent=2)}
        README.md: {readme}

        Based on the above context, identify shared dependencies across the program such as shared
        variables, common utility functions, data schemas, interfaces or classes that need to be 
        consistent and reusable. Provide your response in a JSON structure with the following format:

        {{
            "shared_variables": [],
            "common_utilities": [],
            "data_schemas": [],
            "interfaces": [],
            "classes": []
        }}

        Focus on extracting names and a brief description of the shared dependencies without extra explanations.
        """
        result = self.gpt.chat_with_ollama(systemprompt, self.prompt)
        if isinstance(result, dict):
            result = json.dumps(result)
        print(result)
        return result


    def refine_shared_dependencies(self, filepaths, program_structure):
        # Refine shared dependencies based on actual file paths and program structure
        refined_dependencies = {
            "shared_variables": [],
            "common_utilities": [],
            "data_schemas": [],
            "interfaces": [],
            "classes": []
        }

        # Generate refined dependencies, you could incorporate more logic here
        # Placeholder logic: Identify common utilities or classes from file paths or structure
        for filepath in filepaths:
            # Example: Extract utility functions or common classes based on filepath or structure analysis
            if "utils" in filepath:
                refined_dependencies["common_utilities"].append(filepath)
            # More logic can be added as needed

        print(f"Refined shared dependencies: {json.dumps(refined_dependencies, indent=2)}")
        return refined_dependencies


    def generate_code_for_each_file(self, filepaths_string, program_structure, shared_dependencies=None):
        print("Generating code")
        main_code, unit_tests_code = self.AI_generate_code_and_tests(filepaths_string, program_structure, shared_dependencies)

        # Write both the main code and unit test files to the directory
        self.write_code_and_tests(filepaths_string, main_code, unit_tests_code)

        print(f"Code and unit tests for {filepaths_string} have been generated.")
        return main_code, unit_tests_code

    def AI_generate_code_and_tests(self, filepath, program_structure, shared_dependencies=None):
        new_prompt = f"""
        We are building a program in a structured and test-driven manner. Based on the given program
        structure and shared dependencies, your task is to generate the code for the file '{filepath}' as well
        as the corresponding unit tests to validate its correctness.

        Program Structure: {json.dumps(program_structure, indent=2)}
        Shared Dependencies if applicable: {json.dumps(shared_dependencies, indent=2)}
        Intent of the program: {self.prompt}

        For the file '{filepath}', generate the following:
        - The main code that implements the required functionality.
        - A corresponding set of unit tests that verify the correctness of the implementation.

        Please separate the main code and unit tests clearly, and ensure the unit tests are comprehensive
        and cover the expected behavior of the code.

        Begin generating the code and unit tests now using JSON format following the example:
        {{
            'main_code': ['def add(a, b):\\nreturn a + b'],
            'unit_tests': ['def test_add():\\nassert add(1, 2) == 3']
        
        }}
        """
        
        # Call to AI service with the prompt and return the main code and unit tests.
        # Implement this with the actual machinery to call the generative model or API.
        response = self.gpt.chat_with_ollama(new_prompt, self.prompt)
        
        # Parse the AI's response into main code and unit tests.
        # This could be a simple split in the response, or you might have markers in the
        # response text that indicate where the main code ends and the test code begins.
        # For demonstration purposes, response should be structured as a dict
        # with "main_code" and "unit_tests" fields.
        if isinstance(response, str):
            response = json.loads(response)
        main_code = response['main_code']
        unit_tests_code = response['unit_tests']
        
        return main_code, unit_tests_code
    def write_code_and_tests(self, filepaths_string, main_code, unit_tests_code):
        main_file_path = os.path.join(self.directory, filepaths_string)
        unit_test_file_path = os.path.join(self.directory, "test", f"test_{filepaths_string}")

        # Ensure the directory for the tests exists
        os.makedirs(os.path.dirname(unit_test_file_path), exist_ok=True)

        self.write_docs_to_directory(main_file_path, main_code)
        self.write_docs_to_directory(unit_test_file_path, unit_tests_code)
    
    def write_docs_to_directory(self, filepath, filecode):
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
    
        with open(filepath, "a") as f:
            f.write(str(filecode))


    def write_files_to_directory(self, filepath, filecode):
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
    
        # Normalize the file path
        file_path = os.path.normpath(os.path.join(self.directory, filepath))
        with open(file_path, "a") as f:
            f.write(filecode)

    def debug_generated_code(self):
        extensions = ['py', 'html', 'js', 'css', 'c', 'rs']
        while True:
            code_files = []
            debug_logs = []
            failure_count = {}  # Keeps track of the number of failures for each function

            for extension in extensions:
                code_files.extend(
                    y for x in os.walk(directory) 
                    for y in glob(os.path.join(x[0], f'*.{extension}'))
                    )
            print("Total number of files:", len(code_files))
            if len(code_files) == 0:
                print("Double check that you have downloaded the repo and set the code_dir variable correctly.")
            all_funcs = []
            unit_tests = []
            for code_file in code_files:
                funcs = list(get_functions(code_file))
                for func in funcs:
                    all_funcs.append(func)
                code_tokens_string = json.dumps(code_file)
                code_tokens = num_tokens_from_string(code_tokens_string)
                if code_tokens < tokenLimit:
                    unit_test = unit_test_agent(code_file)
                else:
                    for func in funcs:
                        unit_test_prompt = unit_test_agent()
                        unit_test = self.gpt.chat_with_ollama(unit_test_prompt, func)
                        unit_tests.append(unit_test)
            if isinstance(all_funcs, dict):
                all_funcs = json.dumps(all_funcs)
            print("Total number of functions:", len(all_funcs))
            df = pd.DataFrame(all_funcs)
            df['code_embedding'] = df['code'].apply(lambda x: self.embedding_agent.get_embedding(x, engine="text-embedding-ada-002")) 
            df['filepath'] = df['filepath'].apply(lambda x: x.replace(directory, ""))
            df.to_csv("functions.csv", index=True)
            df.head()
            debug_code_agent = self.gpt.chat_with_ollama(debug_agent, all_funcs)

            if not debug_code_agent or debug_code_agent.strip().lower() == 'no':
                break
            else:
                print(debug_code_agent)



    def filter_filepaths(filepaths):
        filepaths_list = ast.literal_eval(filepaths)
        return [fp.lstrip('/') for fp in filepaths_list]

