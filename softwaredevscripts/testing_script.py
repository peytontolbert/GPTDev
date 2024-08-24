from agents.testing_agent import TestingAgent

project_path = "./path_to_project"

test_agent = TestingAgent("Testing Agent")
test_agent.run_tests(project_path)
test_agent.generate_test_report()
