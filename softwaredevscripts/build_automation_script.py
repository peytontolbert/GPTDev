from agents.buildautomation_agent import BuildAutomationAgent

project_path = "./path_to_project"

# Initialize the build automation agent
build_agent = BuildAutomationAgent("Build Automation Agent")

# Setup build environment
build_agent.setup_build_environment(project_path)

# Run the build process
build_agent.run_build(project_path)

# Generate build report
build_agent.generate_build_report()

