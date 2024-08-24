from agents.integrationtesting_agent import IntegrationTestingAgent

project_path = "./path_to_project"

# Initialize the integration testing agent
integration_test_agent = IntegrationTestingAgent("Integration Testing Agent")

# Run integration tests
integration_test_agent.run_integration_tests(project_path)

# Generate integration test report
integration_test_agent.generate_integration_report()

