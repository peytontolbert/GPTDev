import os
import json
from datetime import datetime, timedelta
from agents.projectplanningagent import ProjectPlanningAgent


def test_clarify_prompt():
    agent = ProjectPlanningAgent(prompt="Test Project", directory=".")
    clarified_prompt = agent.clarify_prompt()
    assert isinstance(clarified_prompt, str), "Clarified prompt should be a string"


def test_add_task():
    agent = ProjectPlanningAgent(prompt="Test Project", directory=".")
    agent.add_task("Task 1", 5)
    assert len(agent.plan["tasks"]) == 1, "There should be one task in the plan"
    assert (
        agent.plan["tasks"][0]["task_name"] == "Task 1"
    ), "Task name should be 'Task 1'"


def test_add_milestone():
    agent = ProjectPlanningAgent(prompt="Test Project", directory=".")
    milestone_date = datetime.now() + timedelta(days=10)
    agent.add_milestone("Milestone 1", milestone_date)
    assert (
        len(agent.plan["milestones"]) == 1
    ), "There should be one milestone in the plan"
    assert (
        agent.plan["milestones"][0]["milestone_name"] == "Milestone 1"
    ), "Milestone name should be 'Milestone 1'"


def test_generate_plan():
    agent = ProjectPlanningAgent(prompt="Test Project", directory=".")
    agent.add_task("Task 1", 5)
    agent.add_milestone("Milestone 1", datetime.now() + timedelta(days=10))
    agent.generate_plan()
    plan_path = "./Test Project_plan.json"
    assert os.path.exists(plan_path), "Plan file should be created"
    with open(plan_path, "r") as file:
        plan = json.load(file)
    assert (
        plan["project_name"] == "Test Project"
    ), "Project name should be 'Test Project'"
    os.remove(plan_path)


def test_generate_readme_and_docs():
    agent = ProjectPlanningAgent(prompt="Test Project", directory=".")
    agent.generate_readme_and_docs()
    readme_path = "./README.md"
    documentation_path = "./DOCUMENTATION.md"
    assert os.path.exists(readme_path), "README.md should be created"
    assert os.path.exists(documentation_path), "DOCUMENTATION.md should be created"
    os.remove(readme_path)
    os.remove(documentation_path)


if __name__ == "__main__":
    test_clarify_prompt()
    test_add_task()
    test_add_milestone()
    test_generate_plan()
    test_generate_readme_and_docs()
    print("All tests passed!")
