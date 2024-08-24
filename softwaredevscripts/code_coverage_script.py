from agents.codecoverage_agent import CodeCoverageAgent

# Initialize agent
code_coverage_agent = CodeCoverageAgent('CodeCoverageAgent')

# Define the main function
def main(project_path):
    # Step 1: Run code coverage
    code_coverage_agent.run_code_coverage(project_path)
    
    # Step 2: Generate coverage report
    code_coverage_agent.generate_coverage_report()

# Example usage
if __name__ == '__main__':
    example_project_path = './path_to_project'
    main(example_project_path)

