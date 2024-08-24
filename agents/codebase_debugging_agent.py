from chat.chat_with_ollama import ChatGPT
from base_agent import Agent
import os
import json
import pandas as pd
from glob import glob
from utils.token_utils import num_tokens_from_string
from src.codesearch import get_functions, get_embedding

class DebuggingAgent(Agent):
    def __init__(self, name, directory):
        super().__init__(name)
        self.gpt = ChatGPT()
        self.directory = directory

    def debug_generated_code(self):
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
                funcs = list(get_functions(code_file))
                for func in funcs:
                    all_funcs.append(func)
                code_tokens_string = json.dumps(code_file)
                code_tokens = num_tokens_from_string(code_tokens_string)
                if code_tokens < 50000:
                    unit_test = self.gpt.chat_with_ollama("Generate unit tests for the following code:", code_file)
                else:
                    for func in funcs:
                        unit_test_prompt = "Generate unit tests for the following function:"
                        unit_test = self.gpt.chat_with_ollama(unit_test_prompt, func)
                        unit_tests.append(unit_test)
            if isinstance(all_funcs, dict):
                all_funcs = json.dumps(all_funcs)
            self.log(f"Total number of functions: {len(all_funcs)}")
            df = pd.DataFrame(all_funcs)
            df["code_embedding"] = df["code"].apply(
                lambda x: get_embedding(x, engine="text-embedding-ada-002")
            )
            df["filepath"] = df["filepath"].apply(lambda x: x.replace(self.directory, ""))
            df.to_csv("functions.csv", index=True)
            df.head()
            debug_code_agent = self.gpt.chat_with_ollama("Debug the following code:", all_funcs)

            if not debug_code_agent or debug_code_agent.strip().lower() == "no":
                break
            else:
                self.log(debug_code_agent)

