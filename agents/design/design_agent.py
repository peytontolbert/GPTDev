# Import necessary modules
import os
import json
from agents.communication.prompt_clarification_agent import PromptClarificationAgent
from agents.design.design_generation_agent import DesignGenerationAgent
from agents.communication.response_parsing_agent import ResponseParsingAgent
from agents.documentation.documentation_generation_agent import DocumentationGenerationAgent
from agents.base_agent import Agent

class DesignAgent(Agent):
    def __init__(self, prompt, directory):
        self.prompt = prompt
        self.directory = directory
        self.prompt_agent = PromptClarificationAgent('PromptClarificationAgent')
        self.design_agent = DesignGenerationAgent('DesignGenerationAgent')
        self.response_agent = ResponseParsingAgent('ResponseParsingAgent')
        self.documentation_agent = DocumentationGenerationAgent('DocumentationGenerationAgent')

    def execute(self, input_data):
        # Generate the prompt
        clarified_prompt = self.prompt_agent.clarify_prompt(input_data)
        
        # Generate the design
        design_response = self.design_agent.generate_design(clarified_prompt)
        
        # Parse the response
        program_design = self.response_agent.parse_response(design_response)
        
        # Generate the design documentation
        self.generate_design_docs(program_design)

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

