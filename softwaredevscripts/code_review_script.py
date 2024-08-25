from agents.analysis.analysis.codereview_agent import CodeReviewAgent

project_path = "./path_to_project"

agent = CodeReviewAgent("Code Review Agent")
agent.review_code(project_path)
agent.generate_review_report()
