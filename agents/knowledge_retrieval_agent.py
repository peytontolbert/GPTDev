from agents.base_agent import Agent
import json
import os

class KnowledgeRetrievalAgent(Agent):
    def __init__(self, name):
        super().__init__(name)

    def execute(self, input_data):
        prompt = self.generate_prompt(input_data)
        detailed_prompt = self.clarify_prompt(prompt)
        response = self.gpt.chat_with_ollama(detailed_prompt, self.name)
        return self.parse_response(response)

    def generate_prompt(self, input_data):
        return (
            f"Given the following task or code:\n{input_data}\n\n"
            "Search external knowledge sources (e.g., GitHub repositories, Stack Overflow, documentation databases) "
            "to find relevant information, code snippets, or best practices that can be used to improve the task. "
            "Summarize the findings in a JSON object with 'source' and 'content' as keys."
        )
    
    
    def get_agent_details(self, directory, agent_name, agent_details, prompt):
        if agent_name not in agent_details:
            agent_file = f"{agent_name}.py"
            with open(os.path.join(directory, agent_file), 'r') as f:
                agent_code = f.read()
            
            details_prompt = (
                f"{prompt}\n"
                f"Analyze the following agent code and provide:\n"
                f"1. A brief summary of its functionality and key methods\n"
                f"2. A list of other agents or modules it depends on. Reply in JSON FORMAT\n\n[AGENT CODE]\n"
            )
            print(f"self prompt: {prompt}")
            print(f"agent code: {agent_code}")
            response = self.gpt.chat_with_ollama(details_prompt, agent_code)
            print(f"raw response: {response}")
            parsed_response = self.parse_response(response)
            print(f"parsed response: {parsed_response}")
            agent_details[agent_name] = parsed_response['summary']
            dependencies = parsed_response.get('dependencies', [])

        return agent_details[agent_name], dependencies

