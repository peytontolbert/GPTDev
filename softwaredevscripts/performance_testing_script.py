from agents.performancetesting_agent import PerformanceTestingAgent

project_path = "./path_to_project"

perf_test_agent = PerformanceTestingAgent("Performance Testing Agent")
perf_test_agent.run_performance_tests(project_path)
perf_test_agent.generate_performance_report()
