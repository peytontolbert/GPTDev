from agents.unittestcreation_agent import UnitTestCreationAgent

project_path = "./path_to_project"

agent = UnitTestCreationAgent("Unit Test Creation Agent")
agent.create_unit_tests(project_path)
agent.save_unit_tests()
