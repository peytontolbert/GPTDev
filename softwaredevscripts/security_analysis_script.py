from agents.analysis.analysis.securityanalysis_agent import SecurityAnalysisAgent

project_path = "./path_to_project"

security_agent = SecurityAnalysisAgent("Security Analysis Agent")
security_agent.run_security_analysis(project_path)
security_agent.generate_security_report()
