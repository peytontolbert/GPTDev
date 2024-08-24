from agents.logging_agent import LoggingAgent

project_path = "./path_to_project"

# Initialize the logging agent
log_agent = LoggingAgent("Logging Agent")

# Setup logging
log_agent.setup_logging(project_path)

# Start logging
log_agent.start_logging()

