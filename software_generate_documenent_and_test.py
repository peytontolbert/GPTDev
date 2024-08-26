from agents.code_generation.codegeneration_agent import CodeGenerationAgent
from agents.documentation.documentation_generation_agent import DocumentationGenerationAgent
from agents.testing.testing_agent import TestingAgent
from agents.testing.test_unit_agent import TestUnitAgent
# Initialize the agents with the necessary configurations
code_generation_agent = CodeGenerationAgent(name="CodeGenerationAgent")
documentation_generation_agent = DocumentationGenerationAgent(name="DocumentationGenerationAgent")
testing_agent = TestingAgent(name="TestingAgent")
test_unit_agent = TestUnitAgent("tests")

def software_generation_from_prompt(prompt, agent_name):
    # Step 1: Generate code based on the user prompt
    generated_code = code_generation_agent.generate_prompt(prompt)
    code_generation_agent.execute(prompt)

    # Step 2: Generate documentation for the generated code
    documentation_generation_agent.generate_documentation_from_code(generated_code)
    test_units = test_unit_agent.execute(generated_code)
    # Step 3: Execute tests for the generated code
    test_results = testing_agent.execute(agent_name, generated_code)

    # If tests fail, handle the test failure and attempt to fix the code
    if test_results != {"status": "success"}:
        fixed_code = testing_agent.handle_test_failure(agent_name, test_results, generated_code)
        print("Fixed Code:", fixed_code)
        # Optionally re-run tests after fixing
        re_test_results = testing_agent.execute(agent_name, fixed_code)
        if re_test_results == {"status": "success"}:
            print("Tests passed after fix.")
        else:
            print("Tests failed again after fix.")
    else:
        print("All tests passed.")

    return generated_code, test_results

# Example usage
prompt = "Create a Python script that implements a basic web server."
agent_name = "web_server_agent"
generated_code, test_results = software_generation_from_prompt(prompt, agent_name)
print("Generated Code:", generated_code)
print("Test Results:", test_results)
