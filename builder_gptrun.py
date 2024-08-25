import os
from builder_gpt import BuilderGPT  # Assuming BuilderGPT is in builder_gpt.py

def automated_task_execution(task_description):
    # Specify the directory where your agents and other resources are located
    directory = os.path.dirname(os.path.abspath(__file__))

    # Initialize BuilderGPT with necessary parameters
    builder_gpt = BuilderGPT(
        name="BuilderGPT",
        prompt="You are a highly efficient BuilderGPT model designed to autonomously improve and manage software development tasks.",
        directory=directory
    )

    # Run the full process, including task execution and agent optimization
    results = builder_gpt.execute(task_description)
    
    # Output the results
    print("Task Execution Results:")
    for result in results:
        print(result)

    # Optionally, after execution, run a process to further optimize agents
    print("\nStarting recursive agent optimization...\n")
    agent_list = os.listdir(directory)  # Assuming agents are in the same directory
    optimized_agents = builder_gpt.agent_improvement_agent.recursive_agent_optimization(agent_list)
    
    print("Optimized Agents:")
    for agent in optimized_agents:
        print(agent)

if __name__ == "__main__":
    # Provide a sample task description to the builder
    sample_task_description = "Build and deploy a scalable web application with a front-end, back-end, database integration, and continuous deployment pipeline."

    # Run the automated task execution
    automated_task_execution(sample_task_description)