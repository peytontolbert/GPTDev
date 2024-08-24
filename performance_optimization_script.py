from agents.performance_monitoring_agent import PerformanceMonitoringAgent
from agents.performanceoptimization_agent import PerformanceOptimizationAgent
from agents.code_generation_agent import CodeGenerationAgent

# Initialize agents
performance_monitoring_agent = PerformanceMonitoringAgent('PerformanceMonitoringAgent')
performance_optimization_agent = PerformanceOptimizationAgent('PerformanceOptimizationAgent')
code_generation_agent = CodeGenerationAgent('CodeGenerationAgent')

# Define the main function
def main(directory, prompt=None):
    # Step 1: Monitor performance
    performance_data = performance_monitoring_agent.execute(directory)
    
    # Step 2: Optimize performance
    optimized_code = performance_optimization_agent.execute(performance_data)
    
    # Step 3: Generate optimized code
    final_code = code_generation_agent.execute(optimized_code, prompt)
    
    # Save the optimized code
    with open(f'{directory}/optimized_code.py', 'w') as code_file:
        code_file.write(final_code)

# Example usage
if __name__ == '__main__':
    example_directory = 'path/to/codebase'
    example_prompt = 'Optimize the code for better performance.'
    main(example_directory, example_prompt)

