import os
import openai
import json
from glob import glob
from typing import List, Dict, Any

from dotenv import load_dotenv
from openai.embeddings_utils import get_embedding

from utils.utils import (
    get_file_content,
    get_function_name,
    get_until_no_space,
    num_tokens_from_string,
    save_embedded_code,
)
from prompts.codeagents import (
    code_documentation_agent,
    code_algorithm_agent,
    code_design_agent,
    code_prompt_agent,
)
from chat.chat_with_ollama import ChatGPT

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
"""

# --- Code Processing Functions ---


def extract_functions(filepath: str) -> List[Dict[str, str]]:
    """
    Extracts all functions from a Python file.
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


# --- Documentation Generation Functions ---


def generate_documentation(code: str) -> str:
    """
    Generates documentation for a piece of code using the code_documentation_agent.
    """
    return ChatGPT.chat_with_ollama(code, code_documentation_agent())


# --- Code Analysis Functions ---


def generate_algorithm(code: str) -> str:
    """
    Generates an algorithm representation from code using the code_algorithm_agent.
    """
    return ChatGPT.chat_with_ollama(code, code_algorithm_agent())


def generate_design(code: str) -> str:
    """
    Generates a design description from code using the code_design_agent.
    """
    return ChatGPT.chat_with_ollama(code, code_design_agent())


# --- Prompt Generation Functions ---


def generate_prompt_from_docs(docs_string: str) -> str:
    """
    Generates a prompt from documentation using the code_prompt_agent.
    """
    return ChatGPT.chat_with_ollama(docs_string, code_prompt_agent())


def create_prompts_from_algorithms_and_designs(
    algorithms: List[str], designs: List[str]
) -> List[str]:
    """
    Combines algorithms and designs into individual prompts.
    """
    prompts = []
    for algorithm, design in zip(algorithms, designs):
        prompt = "Algorithm: " + algorithm + "\nDesign: " + design
        prompts.append(prompt)
    return prompts


class CodebasetoPromptAgent(Agent):
    """
    An agent that converts code into prompts suitable for AI models.
    """

    def __init__(self, token_limit: int = 50000):
        """
        Initializes the CodeToPromptAgent with a token limit.

        Args:
            token_limit (int):
                    token_limit (int): The maximum number of tokens to process.
        """
        super().__init__()
        self.token_limit = token_limit

    def perform_task(self, directory):
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
        """
        all_docs_string = json.dumps(all_docs)
        tokens = num_tokens_from_string(all_docs_string)
        save_embedded_code(all_funcs, clone_dir, "functions", "code")
        save_embedded_code(all_docs, clone_dir, "documentations", "doc")

        if tokens < self.token_limit:
            print("Tokens within limit. Generating prompt from all docs...")
            prompt = generate_prompt_from_docs(all_docs_string)
        else:
            print("Tokens exceed limit. Generating prompts from chunked data...")
            algorithms = [generate_algorithm(json.dumps(doc)) for doc in all_docs]
            designs = [generate_design(json.dumps(doc)) for doc in all_docs]
            prompts = create_prompts_from_algorithms_and_designs(algorithms, designs)
            prompts_string = json.dumps(prompts)
            prompts_tokens = num_tokens_from_string(prompts_string)
            if prompts_tokens < self.token_limit:
                print("Generating prompt from algorithms and designs...")
                prompt = generate_prompt_from_docs(prompts_string)
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
        """
        code = get_file_content(code_file)
        if code is None:
            return []

        tokens = num_tokens_from_string(code)
        docs: List[Dict[str, str]] = []

        if tokens < self.token_limit:
            print("Code within limit. Summarizing the entire code...")
            doc_text = generate_documentation(code)
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
                    doc = generate_documentation("\n\n".join(function_list))
                    docs.append(doc)
                    function_list = [func["code"]]
                    current_tokens = num_tokens_from_string(func["code"])

            if function_list:
                doc = generate_documentation("\n\n".join(function_list))
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
