import openai
import os
import json
import time
import sys

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from chat.chat_with_ollama import ChatGPT
from agents.codingagents import clarifying_agent

class BuilderGPT:
    def __init__(self, prompt, directory):
        self.prompt = prompt
        self.directory = directory
        self.model = 'gpt-4-1106-preview'  # Set your default model here
        self.gpt = ChatGPT()

def clarify_prompt(self):
        while True:
            clarifying_prompt = clarifying_agent()
            clarifying_prompt += (
                '\n\n'
                'Is anything unclear? If yes, only answer in the form:\n'
                '{remaining unclear areas} remaining questions. \n'
                '{Next question}\n'
                'If everything is sufficiently clear, only answer "no".'
            )
            clarifying_questions = self.gpt.chat_with_ollama(clarifying_prompt, self.prompt)
            if "no" in clarifying_questions.lower():
                break
            self.prompt += clarifying_questions + "\n"
        return json.dumps(self.prompt)

    def parse_response(self, response):
        if response and isinstance(response, str):
            try:
                program_design = json.loads(response)
                return program_design
            except json.JSONDecodeError:
                print("Failed to decode JSON. Handling as a string or other format.")
                return None
        elif isinstance(response, (dict, list)):
            return response
        else:
            print("Unexpected data type received.")
            return None

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
        - Recursive improvements and self-optimization strategies
        - Error handling and logging mechanisms
        - Testing strategies and coverage
        """
        
        response = self.gpt.chat_with_ollama(systemprompt, self.prompt)
        return self.parse_response(response)
    


def improve_codebase(self):
        print("Improving the codebase...")
        
        # Step 1: Analyze the current codebase
        file_paths = get_file_paths(self.directory)
        for file_path in file_paths:
            file_content = get_file_content(file_path)
            improvement_prompt = f"Analyze the following code and suggest improvements:\n\n{file_content}"
            
            # Step 2: Generate improved code
            improved_code = self.gpt.chat_with_ollama(improvement_prompt, self.prompt)
            
            # Step 3: Apply the improvements
            write_file(file_path, improved_code)
            print(f"Improved {file_path}")
            
            # Step 4: Recursively improve the code
            recursive_prompt = f"Analyze the improved code and suggest further improvements:\n\n{improved_code}"
            further_improved_code = self.gpt.chat_with_ollama(recursive_prompt, self.prompt)
            write_file(file_path, further_improved_code)
            print(f"Further improved {file_path}")
        pass



    def expand_codebase(self):
        print("Expanding the codebase...")
        
        # Step 1: Identify new features or modules
        expansion_prompt = f"Based on the current codebase and the following requirements, suggest new features or modules to add:

{self.prompt}"
        
        # Step 2: Generate new code for the features or modules
        new_code = self.gpt.chat_with_ollama(expansion_prompt, self.prompt)
        
        # Step 3: Integrate the new code into the existing codebase
        new_module_path = os.path.join(self.directory, 'new_module.py')
        write_file(new_module_path, new_code)
        print(f"Added new module: {new_module_path}")
        pass

if __name__ == "__main__":
    prompt = "Your initial prompt here"
    directory = "path/to/your/directory"
    builder_gpt = BuilderGPT(prompt, directory)
    builder_gpt.clarify_prompt()
    program_structure = builder_gpt.design_program_structure()
    print(program_structure)
