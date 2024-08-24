from agents.dependencymanagement_agent import DependencyManagementAgent

project_path = "./path_to_project"

dep_mgmt_agent = DependencyManagementAgent("Dependency Management Agent")
dep_mgmt_agent.check_dependencies(project_path)
dep_mgmt_agent.update_dependencies(project_path)
