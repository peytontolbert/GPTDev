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
        # Step 1: Analyze and optimize the agents list
        optimization_suggestions = self.analyze_and_optimize_agents()

        # Step 2: Use the optimization suggestions to potentially expand the agent list
        expanded_agent_list = self.expand_agent_list(optimization_suggestions)

        # Step 3: Load the agents from the optimized and expanded list
        selected_agents = self.dynamic_selection(expanded_agent_list)

        # Step 4: Execute the selected agents
        results = self.run_selected_agents(selected_agents, input_data)
        
        # Return the combined results
        return results

    def analyze_with_ollama(self):
        # Generates a prompt to analyze the current state of agents
        analysis_prompt = (
            "Analyze the current list of agents in the directory. "
            "Identify areas for improvement or expansion. "
            "Suggest new agents that can enhance the overall system."
        )
        analysis_result = self.gpt.chat_with_ollama(analysis_prompt, self.prompt)
        return analysis_result

    def dynamic_selection(self, agent_list):
        # Select agents from the provided agent list
        selected_agents = []

        for agent in agent_list:
            if agent in os.listdir(self.directory):
                selected_agents.append(agent)

        return selected_agents

    def run_selected_agents(self, agents, input_data):
        results = []
        
        for agent in agents:
            agent_module = importlib.import_module(f'agents.{agent}')
            agent_instance = agent_module.AgentClass()  # Assuming each agent has a class called 'AgentClass'
            result = agent_instance.execute(input_data)
            results.append(result)
        
        return results

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
                module_name = filename[:-3]  # Remove the .py extension
                module = importlib.import_module(f'agents.{module_name}')
                agent_class = getattr(module, 'AgentClass', None)
                if agent_class:
                    agents[module_name] = agent_class()
        
        return agents

    def analyze_and_optimize_agents(self):
        # Step 1: Generate a summary of all agents and their functions
        agents_summary = "Summary of all agents and their functions:\\n"
        for agent_file in os.listdir(self.directory):
            if agent_file.endswith('_agent.py'):
                with open(os.path.join(self.directory, agent_file), 'r') as f:
                    agent_code = f.read()
                agents_summary += f"Agent: {agent_file}\\n{agent_code}\\n\\n"

        # Step 2: Loop through each agent and analyze with Ollama for decomposition/optimization
        optimization_suggestions = []
        for agent_file in os.listdir(self.directory):
            if agent_file.endswith('_agent.py'):
                with open(os.path.join(self.directory, agent_file), 'r') as f:
                    agent_code = f.read()
                
                agent_analysis_prompt = (
                    f"Here is the code for the agent {agent_file}:\\n{agent_code}\\n"
                    "Analyze this agent and suggest whether it can be decomposed into smaller agents or optimized. "
                    "If optimization or decomposition is possible, provide specific recommendations."
                )
                analysis_result = self.gpt.chat_with_ollama(agent_analysis_prompt, agents_summary)
                optimization_suggestions.append((agent_file, analysis_result))
        
        return optimization_suggestions

    def expand_agent_list(self, optimization_suggestions):
        # Expands the agent list based on optimization suggestions from Ollama
        expanded_agent_list = []
        
        for agent_file, suggestions in optimization_suggestions:
            expanded_agent_list.append(agent_file)  # Include the original agent
            
            # Review for preexisting agents to avoid duplication
            for existing_agent_file in os.listdir(self.directory):
                if existing_agent_file.endswith('_agent.py') and existing_agent_file != agent_file:
                    with open(os.path.join(self.directory, existing_agent_file), 'r') as f:
                        existing_agent_code = f.read()
                    
                    # Create a prompt for LLM to compare and decide on function reuse or addition
                    comparison_prompt = (
                        f"Compare the agent {agent_file} with the existing agent {existing_agent_file}.\\n"
                        f"Here is the code for {agent_file}:\\n{suggestions}\\n"
                        f"Here is the code for {existing_agent_file}:\\n{existing_agent_code}\\n"
                        "Decide whether to reuse existing functions from the preexisting agent or add new functions "
                        "to facilitate the decomposition of the agent. Include the reasons for your decisions."
                    )
                    comparison_result = self.gpt.chat_with_ollama(comparison_prompt, "")
                    
                    # Process the LLM's decision on whether to reuse functions or add new ones
                    if isinstance(comparison_result, dict):
                        if "reuse_functions" in comparison_result:
                            expanded_agent_list.append(existing_agent_file)
                        if "new_functions" in comparison_result:
                            expanded_agent_list.extend(comparison_result["new_functions"])
        
        return expanded_agent_list