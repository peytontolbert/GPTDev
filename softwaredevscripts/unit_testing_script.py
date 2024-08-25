from agents.analysis.analysis.unittesting_agent import UnitTestingAgent

# Initialize agent
unit_testing_agent = UnitTestingAgent('UnitTestingAgent')

# Define the main function
def main(project_path):
    # Step 1: Run unit tests
    unit_testing_agent.run_unit_tests(project_path)
    
    # Step 2: Generate test report
    unit_testing_agent.generate_test_report()

# Example usage
if __name__ == '__main__':
    example_project_path = './path_to_project'
    main(example_project_path)

