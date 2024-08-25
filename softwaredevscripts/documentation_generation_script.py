from agents.analysis.analysis.documentationgeneration_agent import DocumentationGenerationAgent

# Initialize agent
documentation_generation_agent = DocumentationGenerationAgent('DocumentationGenerationAgent')

# Define the main function
def main(project_path):
    # Step 1: Generate documentation
    documentation_generation_agent.generate_documentation(project_path)

# Example usage
if __name__ == '__main__':
    example_project_path = './path_to_project'
    main(example_project_path)

