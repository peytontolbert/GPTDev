from agents.staticanalysis_agent import StaticAnalysisAgent

project_path = "./path_to_project"

static_analysis_agent = StaticAnalysisAgent("Static Analysis Agent")
static_analysis_agent.run_static_analysis(project_path)
static_analysis_agent.generate_analysis_report()
