import openai
import os
import json
import time
import sys
import importlib
from base_agent import Agent
from chat.chat_with_ollama import ChatGPT

class BuilderGPT(Agent):
    def __init__(self, name, prompt, directory):
        super().__init__(name)
        self.prompt = prompt
        self.directory = directory
        self.gpt = ChatGPT()

    def execute(self, input_data):
        self.improved_dynamic_agent_loader(self.directory)
        # Function is incomplete, please finish

    def generate_prompt(self, input_data):
        # Implement prompt generation logic here
        pass

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

    def dynamic_agent_loader(self, agent_directory):
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

    def create_new_agent(self, agent_name, agent_code):
        agent_path = os.path.join(self.directory, f"{agent_name}.py")
        with open(agent_path, 'w') as agent_file:
            agent_file.write(agent_code)
        return agent_path

    def reflect_and_improve(self, agent_name):
        agent_path = os.path.join(self.directory, f"{agent_name}.py")
        with open(agent_path, 'r') as agent_file:
            agent_code = agent_file.read()
        reflection_prompt = f"Reflect on the following agent code and suggest improvements. Provide detailed suggestions and context where necessary:\n{agent_code}"
        improvements = self.gpt.chat_with_ollama(reflection_prompt)
        return improvements

    def build_and_improve_agent(self, agent_name, agent_code):
        agent_path = self.create_new_agent(agent_name, agent_code)
        improvements = self.reflect_and_improve(agent_name)
        detailed_improvements_prompt = f"Here is the original code:\n{agent_code}\n\nHere are the suggested improvements:\n{improvements}\n\nPlease provide a final improved version of the agent code, incorporating the suggestions and maintaining context."
        final_improvements = self.gpt.chat_with_ollama(detailed_improvements_prompt)
        with open(agent_path, 'w') as agent_file:
            agent_file.write(final_improvements)
        return agent_path

    def enhance_clarify_prompt(self):
        # Enhanced clarify_prompt method
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

    def improved_dynamic_agent_loader(self, agent_directory):
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

    def create_and_improve_agent(self, agent_name, agent_code):
        agent_path = self.create_new_agent(agent_name, agent_code)
        improvements = self.reflect_and_improve(agent_name)
        with open(agent_path, 'w') as agent_file:
            agent_file.write(improvements)
        return agent_path

    def list_agents(self):
        agents = self.dynamic_agent_loader(self.directory)
        return list(agents.keys())

    def expand_agent_list(self, new_agents):
        for agent_name, agent_code in new_agents.items():
            self.create_and_improve_agent(agent_name, agent_code)

    def run_mode(self, mode):
        if mode == 'list':
            return self.list_agents()
        elif mode == 'expand':
            new_agents = self.gpt.chat_with_ollama('Provide new agents to add in JSON format with agent names as keys and agent code as values.')
            new_agents = json.loads(new_agents)
            self.expand_agent_list(new_agents)
        else:
            print('Invalid mode selected.')

