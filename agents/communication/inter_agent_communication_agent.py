import json
from agents.base_agent import Agent

class InterAgentCommunicationAgent(Agent):
    def __init__(self, name, shared_data_store = {}):
        super().__init__(name)
        self.shared_data_store = shared_data_store

    def execute(self, input_data):
        try:
            # Perform the task
            result = self.perform_task(input_data)
            return result
        except Exception as e:
            self.log(f"Error: {str(e)}")
            return None

    def perform_task(self, input_data):
        recipient_agent = input_data.get('recipient_agent')
        message = input_data.get('message')
        if recipient_agent and message:
            self.send_message(recipient_agent, message)
            response = self.receive_message(recipient_agent)
            return response
        else:
            self.log("Invalid input data")
            return None
        
    def send_message(self, recipient_agent, message):
        self.shared_data_store[recipient_agent] = message

    def receive_message(self, sender_agent):
        return self.shared_data_store.get(sender_agent, None)

    def generate_prompt(self, input_data):
        # Implement the prompt generation logic here
        recipient_agent = input_data.get('recipient_agent')
        message = input_data.get('message')
        return f"Send the following message to {recipient_agent}: {message}"

    def parse_response(self, response):
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {"raw_response": response}

