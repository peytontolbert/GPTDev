# Import necessary modules
import openai
import os
import json
from chat.chat_with_ollama import ChatGPT
from agents.base_agent import Agent

# Initialize OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

class DesignAgent(Agent):
    def __init__(self, prompt, directory, model="gpt-4-1106-preview"):
        self.prompt = prompt
        self.directory = directory
        self.gpt = ChatGPT()
        self.model = model

    def execute(self, input_data):
        # Implement the main logic here
        prompt = self.generate_prompt(input_data)
        design_response = self.generate_design(prompt)
        program_design = self.parse_response(design_response)
        self.generate_design_docs(program_design)

    def generate_prompt(self, input_data):
        # Implement prompt generation logic here
        return f"Generate a software design based on the following requirements: {input_data}"

    def generate_design(self, prompt):
        # Call to AI service with the prompt
        response = self.gpt.chat_with_ollama(prompt, self.prompt)
        return response

    def parse_response(self, response):
        # Parse the AI's response into a design document
        try:
            design_doc = json.loads(response)
            return design_doc
        except json.JSONDecodeError:
            print("Failed to decode JSON. Handling as a string or other format.")
            return None

    def generate_design_docs(self, program_design):
        if program_design:
            design_doc_path = os.path.join(self.directory, "DESIGN_DOCUMENT.md")
            design_content = f"# Design Document\n\n{json.dumps(program_design, indent=2)}\n"
            self.write_docs_to_directory(design_doc_path, design_content)
            print(f"Design document created in {self.directory}")

    def write_docs_to_directory(self, filepath, filecode):
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        with open(filepath, "w") as f:
            f.write(filecode)

