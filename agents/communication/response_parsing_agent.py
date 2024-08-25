from agents.base_agent import Agent
import json

class ResponseParsingAgent(Agent):
    def __init__(self, name):
        super().__init__(name)

    def parse_response(self, response):
        if response and isinstance(response, str):
            try:
                parsed_response = json.loads(response)
                return parsed_response
            except json.JSONDecodeError:
                self.log("Failed to decode JSON. Handling as a string or other format.")
                return {"raw_response": response}
        elif isinstance(response, (dict, list)):
            return response
        else:
            self.log("Unexpected data type received.")
            return None

