# Import necessary modules
import openai
import os
import json
from chat.chat_with_ollama import ChatGPT
from agents.base_agent import Agent

# Initialize OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

class MaintenanceAgent(Agent):
    def __init__(self, prompt, directory, model="gpt-4-1106-preview"):
        self.prompt = prompt
        self.directory = directory
        self.gpt = ChatGPT()
        self.model = model

    def execute(self, input_data):
        # Implement the main logic here
        prompt = self.generate_prompt(input_data)
        maintenance_response = self.generate_maintenance_plan(prompt)
        maintenance_plan = self.parse_response(maintenance_response)
        self.generate_maintenance_docs(maintenance_plan)

    def generate_prompt(self, input_data):
        # Implement prompt generation logic here
        return f"Generate a maintenance plan based on the following requirements: {input_data}"

    def generate_maintenance_plan(self, prompt):
        # Call to AI service with the prompt
        response = self.gpt.chat_with_ollama(prompt, self.prompt)
        return response

    def parse_response(self, response):
        # Parse the AI's response into a maintenance plan
        try:
            maintenance_plan = json.loads(response)
            return maintenance_plan
        except json.JSONDecodeError:
            print("Failed to decode JSON. Handling as a string or other format.")
            return None

    def generate_maintenance_docs(self, maintenance_plan):
        if maintenance_plan:
            maintenance_doc_path = os.path.join(self.directory, "MAINTENANCE_PLAN.md")
            maintenance_content = f"# Maintenance Plan\n\n{json.dumps(maintenance_plan, indent=2)}\n"
            self.write_docs_to_directory(maintenance_doc_path, maintenance_content)
            print(f"Maintenance plan document created in {self.directory}")

    def write_docs_to_directory(self, filepath, filecode):
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        with open(filepath, "w") as f:
            f.write(filecode)

