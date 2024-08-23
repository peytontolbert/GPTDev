import openai
import os
import json
import time
import sys
import importlib
from base_agent import Agent

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

    def dynamic_agent_loader(agent_directory):
        agents = {}
        
        for filename in os.listdir(agent_directory):
            if filename.endswith('_agent.py'):
                module_name = filename[:-3]  # Strip off the ".py"
                file_path = os.path.join(agent_directory, filename)
                
                # Load the module dynamically
                spec = importlib.util.spec_from_file_location(module_name, file_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Register all classes inheriting from Agent
                for attribute_name in dir(module):
                    attribute = getattr(module, attribute_name)
                    if isinstance(attribute, type) and issubclass(attribute, Agent) and attribute is not Agent:
                        agent_instance = attribute()
                        agents[attribute_name] = agent_instance
        
        return agents