import os
import json
from chat.chat_with_ollama import ChatGPT

class OptimizationAndGeneralization:
    def __init__(self, directory, gpt, version_control):
        self.directory = directory
        self.gpt = gpt
        self.version_control = version_control


    def optimize_agent(self, agent_name, optimization_details):
        agent_file = f"{agent_name}.py"
        with open(os.path.join(self.directory, agent_file), 'r') as f:
            original_code = f.read()
        
        optimization_prompt = f"Optimize the following agent code based on these details:\n{optimization_details}\n\nOriginal code:\n{original_code}"
        optimized_code = self.gpt.chat_with_ollama(optimization_prompt)
        
        self.save_to_file(os.path.join(self.directory, agent_file), optimized_code)
        
        # Add new version
        changes = f"Optimized agent based on: {optimization_details}"
        new_version = self.version_control.add_version(agent_name, optimized_code, changes)
        
        # Update CHANGELOG.md
        changelog = self.version_control.get_changelog(agent_name)
        self.save_to_file(os.path.join(self.directory, f'{agent_name}_CHANGELOG.md'), changelog)

    def generalize_agent(self, agent_name, generalization_details):
        agent_file = f"{agent_name}.py"
        with open(os.path.join(self.directory, agent_file), 'r') as f:
            original_code = f.read()
        
        generalization_prompt = f"Generalize the following agent code based on these details:\n{generalization_details}\n\nOriginal code:\n{original_code}"
        generalized_code = self.gpt.chat_with_ollama(generalization_prompt)
        
        new_agent_name = f"{generalization_details['new_name']}_agent.py"
        self.save_to_file(os.path.join(self.directory, new_agent_name), generalized_code)
        
        # Add new version
        changes = f"Created generalized agent {generalization_details['new_name']} from {agent_name}"
        self.version_control.add_version(generalization_details['new_name'], generalized_code, changes)
        
        return new_agent_name

    def save_to_file(self, path, content):
        with open(path, 'w') as f:
            f.write(content)

