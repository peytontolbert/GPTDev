from agents.analysis.analysis.codequality_agent import CodeQualityAgent

# Initialize agent
code_quality_agent = CodeQualityAgent('CodeQualityAgent')

# Define the main function
def main(project_path):
    # Step 1: Check code quality
    code_quality_agent.check_code_quality(project_path)
    
    # Step 2: Generate quality report
    code_quality_agent.generate_quality_report()

# Example usage
if __name__ == '__main__':
    example_project_path = './path_to_project'
    main(example_project_path)

