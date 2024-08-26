from agents.planning.task_planning_agent import TaskPlanningAgent
from agents.management.orchestration_agent import OrchestrationAgent
from agents.communication.inter_agent_communication_agent import InterAgentCommunicationAgent
from agents.code_generation.code_generation_agent import CodeGenerationAgent
from agents.testing.testing_agent import TestingAgent
from agents.documentation.documentation_generation_agent import DocumentationGenerationAgent

# Initialize agents
task_planning_agent = TaskPlanningAgent('TaskPlanningAgent')
orchestration_agent = OrchestrationAgent('OrchestrationAgent', {
    'code_generation_agent': CodeGenerationAgent('CodeGenerationAgent'),
    'testing_agent': TestingAgent(),
    'documentation_agent': DocumentationGenerationAgent('DocumentationGenerationAgent')
})
inter_agent_communication_agent = InterAgentCommunicationAgent('InterAgentCommunicationAgent', {})

# Define the main function
def main(requirements):
    # Step 1: Plan the tasks
    task_plan = task_planning_agent.execute(requirements)
    
    # Step 2: Orchestrate the tasks
    orchestration_results = orchestration_agent.execute(task_plan)
    
    # Step 3: Communicate between agents if needed
    communication_results = inter_agent_communication_agent.execute({
        'recipient_agent': 'code_generation_agent',
        'message': requirements
    })
    
    # Step 4: Generate code
    generated_code = orchestration_results['code_generation_agent']
    
    # Step 5: Test the generated code
    test_results = orchestration_results['testing_agent']
    
    # Step 6: Generate documentation
    documentation = orchestration_results['documentation_agent']
    
    # Save the results
    with open('generated_code.py', 'w') as code_file:
        code_file.write(generated_code)
    with open('test_results.txt', 'w') as test_file:
        test_file.write(test_results)
    with open('documentation.md', 'w') as doc_file:
        doc_file.write(documentation)

# Example usage
if __name__ == '__main__':
    example_requirements = 'Create a Python script that reads a CSV file and prints the contents.'
    main(example_requirements)

