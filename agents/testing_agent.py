# agents/testing_agent.py

from agents.base_agent import Agent
import unittest
import json

class TestingAgent(Agent):
    def __init__(self, name):
        super().__init__(name)

    def execute(self, agent_name, agent_code):
        test_suite = unittest.TestLoader().discover(f'tests/{agent_name}')
        test_result = unittest.TextTestRunner().run(test_suite)
        
        if not test_result.wasSuccessful():
            return self.handle_test_failure(agent_name, test_result, agent_code)
        
        return {"status": "success"}

    def handle_test_failure(self, agent_name, test_result, agent_code):
        failed_tests = [str(error[0]) for error in test_result.errors + test_result.failures]
        fix_prompt = (
            f"The following tests failed for agent {agent_name}:\n{failed_tests}\n\n"
            f"Current implementation:\n{agent_code}\n\n"
            "Provide fixes to make the tests pass."
        )
        fixed_code = self.gpt.chat_with_ollama(fix_prompt, self.prompt)
        return fixed_code