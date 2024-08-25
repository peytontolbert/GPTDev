from agents.analysis.analysis.coderefactoring_agent import CodeRefactoringAgent

# Initialize agent
code_refactoring_agent = CodeRefactoringAgent('CodeRefactoringAgent')

# Define the main function
def main(project_path):
    # Step 1: Analyze code
    code_refactoring_agent.analyze_code(project_path)
    
    # Step 2: Refactor code
    code_refactoring_agent.refactor_code()

# Example usage
if __name__ == '__main__':
    example_project_path = './path_to_project'
    main(example_project_path)

