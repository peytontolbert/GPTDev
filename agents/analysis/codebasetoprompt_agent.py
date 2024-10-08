import os
import openai
import json
from glob import glob
from typing import List, Dict, Any
from dotenv import load_dotenv
from utils.code_utils import (
    get_function_name, 
    get_until_no_space
    )
from utils.token_utils import (
    num_tokens_from_string
)
from utils.file_utils import (
    get_file_content,
    save_embedded_code
)
from agents.base_agent import Agent
from chat.chat_with_ollama import ChatGPT
from agents.documentation.documentation_generation_agent import DocumentationGenerationAgent
from agents.design.design_generation_agent import DesignGenerationAgent

# Load environmental variables and set global constants
load_dotenv()
tokenLimit = 50000
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
CLONE_DIR = os.getenv("CLONE_DIR", "")

# Ensure API key is available
if not OPENAI_API_KEY:
    raise ValueError(
        "OpenAI API key not found. Please set it in your environment variables."
    )

openai.api_key = OPENAI_API_KEY

"""
Codebase To Prompt Agent: Traverses a codebase to generate a specific prompt to get an autonomous GPT agent to code the entire repo.

Classes:
    CodebasetoPromptAgent: An agent that converts code into prompts suitable for AI models.

Functions:
    extract_functions(filepath: str) -> List[Dict[str, str]]: Extracts all functions from a Python file.

"""

# --- Code Processing Functions ---


def extract_functions(filepath: str) -> List[Dict[str, str]]:
    """
    Extracts all functions from a Python file.

    Args:
        filepath (str): The path to the Python file.

    Returns:
        List[Dict[str, str]]: A list of dictionaries containing function code and names.
    """
    with open(filepath, "r") as file:
        whole_code = file.read().replace("\r", "\n")
    all_lines = whole_code.split("\n")
    functions = []
    for i, l in enumerate(all_lines):
        if l.startswith("def "):
            code = get_until_no_space(all_lines, i)
            function_name = get_function_name(code)
            functions.append(
                {"code": code, "function_name": function_name, "filepath": filepath}
            )
    return functions


class CodebasetoPromptAgent(Agent):
    """
    An agent that converts code into prompts suitable for AI models.

    Attributes:
        token_limit (int): The maximum number of tokens to process.
        documentation_generation_agent (DocumentationGenerationAgent): Agent for generating documentation.
        design_generation_agent (DesignGenerationAgent): Agent for generating design.
    """

    def __init__(self, token_limit: int = 50000):
        """
        Initializes the CodeToPromptAgent with a token limit.

        Args:
            token_limit (int): The maximum number of tokens to process.
        """
        super().__init__()
        self.token_limit = token_limit
        self.documentation_generation_agent = DocumentationGenerationAgent()
        self.design_generation_agent = DesignGenerationAgent()

    def perform_task(self, directory):
        """
        Performs the task of generating prompts for code files in a directory.

        Args:
            directory (str): The directory containing the code files.
        """
        code_files = [
            y
            for x in os.walk(directory)
            for ext in (
                "*.py",
                "*.js",
                "*.cpp",
                "*.rs",
                "*.md",
                "*.txt",
                "*.html",
            )
            for y in glob(os.path.join(x[0], ext))
        ]
        if not code_files:
            print("No code files found in the specified directory.")
            return
        self.generate_prompts_for_files(code_files, directory)
        pass

    def generate_prompt(self, input_data):
        """
        Generates a prompt from the input data.

        Args:
            input_data (str): The input data to generate the prompt from.
        """
        # Implement codebase to prompt logic here
        pass

    def generate_prompts_for_files(self, code_files: List[str], clone_dir: str) -> None:
        """
        Generates prompts from code files and saves them to a file.

        Args:
            code_files (List[str]): List of paths to code files.
            clone_dir (str): Directory path where the code resides.
        """
        all_funcs: List[Dict[str, str]] = []
        all_docs: List[Dict[str, str]] = []

        for code_file in code_files:
            docs = list(self._chunk_and_summarize(code_file))
            funcs = extract_functions(code_file)

            # Skip the file if both docs and funcs are empty
            if not docs and not funcs:
                print(f"Skipping empty or non-processable file: {code_file}")
                continue

            all_funcs.extend(funcs)
            all_docs.extend(docs)

        if all_docs:
            self._process_and_save_prompts(all_funcs, all_docs, clone_dir)

    def _process_and_save_prompts(
        self,
        all_funcs: List[Dict[str, str]],
        all_docs: List[Dict[str, str]],
        clone_dir: str,
    ) -> None:
        """
        Processes documentation data and generates prompts based on token limits.

        Args:
            all_funcs (List[Dict[str, str]]): List of all functions extracted from code files.
            all_docs (List[Dict[str, str]]): List of all documentation extracted from code files.
            clone_dir (str): Directory path where the code resides.
        """
        all_docs_string = json.dumps(all_docs)
        tokens = num_tokens_from_string(all_docs_string)
        save_embedded_code(all_funcs, clone_dir, "functions", "code")
        save_embedded_code(all_docs, clone_dir, "documentations", "doc")

        if tokens < self.token_limit:
            print("Tokens within limit. Generating prompt from all docs...")
            prompt = self.generate_prompt_from_docs(all_docs_string)
        else:
            print("Tokens exceed limit. Generating prompts from chunked data...")
            algorithms = [self.generate_algorithm(json.dumps(doc)) for doc in all_docs]
            designs = [self.generate_design(json.dumps(doc)) for doc in all_docs]
            prompts = self.create_prompts_from_algorithms_and_designs(algorithms, designs)
            prompts_string = json.dumps(prompts)
            prompts_tokens = num_tokens_from_string(prompts_string)
            if prompts_tokens < self.token_limit:
                print("Generating prompt from algorithms and designs...")
                prompt = self.generate_prompt_from_docs(prompts_string)
            else:
                print("Tokens still exceed limit. Saving chunked prompts to file...")
                self._save_prompts_to_file(prompts, "prompts.txt")
                return

        print(f"Prompt: {prompt}")
        self._save_prompts_to_file(prompt, "prompts.txt")
        print(f"Total number of functions: {len(all_funcs)}")

    def _chunk_and_summarize(self, code_file: str) -> List[Dict[str, str]]:
        """
        Chunks code into smaller parts and summarizes each part.

        Args:
            code_file (str): The path to the code file.

        Returns:
            List[Dict[str, str]]: A list of dictionaries containing summarized documentation and code.
        """
        code = get_file_content(code_file)
        if code is None:
            return []

        tokens = num_tokens_from_string(code)
        docs: List[Dict[str, str]] = []

        if tokens < self.token_limit:
            print("Code within limit. Summarizing the entire code...")
            doc_text = self.documentation_generation_agent.generate_documentation_from_code(code)
            docs.append({"doc": doc_text, "code": code, "filepath": code_file})
        else:
            print("Code exceeds limit. Chunking and summarizing...")
            funcs = extract_functions(code_file)
            function_list: List[str] = []
            current_tokens = 0

            for func in funcs:
                potential_tokens = current_tokens + num_tokens_from_string(func["code"])
                if potential_tokens < self.token_limit:
                    function_list.append(func["code"])
                    current_tokens = potential_tokens
                else:
                    doc = self.documentation_generation_agent.generate_documentation_from_code("\n\n".join(function_list))
                    docs.append(doc)
                    function_list = [func["code"]]
                    current_tokens = num_tokens_from_string(func["code"])

            if function_list:
                doc = self.documentation_generation_agent.generate_documentation_from_code("\n\n".join(function_list))
                docs.append(doc)

        return docs

    def _save_prompts_to_file(self, prompts: List[str], filename: str) -> None:
        """
        Save the generated prompts to a text file.

        Args:
            prompts (List[str]): The prompts to be saved.
            filename (str): The name of the file where prompts will be saved.
        """
        with open(filename, "a") as file:
            for prompt in prompts:
                file.write(prompt + "\n\n")


def main():
    """
    Main function to execute the code conversion process.
    """
    code_files = [
        y
        for x in os.walk(CLONE_DIR)
        for ext in (
            "*.py",
            "*.js",
            "*.cpp",
            "*.rs",
            "*.md",
            "*.txt",
            "*.html",
        )
        for y in glob(os.path.join(x[0], ext))
    ]
    if not code_files:
        print("No code files found in the specified directory.")
        return
    converter = CodebasetoPromptAgent(tokenLimit)
    converter.generate_prompts_for_files(code_files, CLONE_DIR)


if __name__ == "__main__":
    main()



