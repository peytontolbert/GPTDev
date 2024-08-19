from agents.documentationagent import DocumentationAgent

# Set the directory to the current working directory
directory = "."

# Create an instance of the DocumentationAgent
doc_agent = DocumentationAgent(directory)

# Generate README.md and DOCUMENTATION.md
doc_agent.generate_readme()
doc_agent.generate_documentation()
