from agents.documentation_agent import DocumentationAgent

project_path = "./path_to_project"

doc_agent = DocumentationAgent("Documentation Agent")
doc_agent.generate_documentation(project_path)
doc_agent.save_documentation()
