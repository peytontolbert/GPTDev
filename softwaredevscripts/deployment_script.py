from agents.analysis.analysis.deployment_agent import DeploymentAgent

project_path = "./path_to_project"

agent = DeploymentAgent("Deployment Agent")
agent.prepare_deployment(project_path)
agent.deploy_project()
