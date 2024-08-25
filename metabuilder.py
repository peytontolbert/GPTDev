import time
import json
from builder_gpt import BuilderGPT
from agents.management.task_manager_agent import TaskManagerAgent

class MetaScript:
    def __init__(self, builder_gpt):
        self.builder_gpt = builder_gpt
        self.task_queue = []
        self.completed_tasks = []
        self.task_manager_agent = TaskManagerAgent(name="TaskManagerAgent", agents={
            'task_decomposition': builder_gpt.task_decomposition_agent,
            'knowledge_retrieval': builder_gpt.knowledge_retrieval_agent,
            'code_review': builder_gpt.code_review_agent,
            'meta_learning': builder_gpt.meta_learning_agent,
            'exploration_strategy': builder_gpt.exploration_strategy_agent,
            'performance_evaluation': builder_gpt.performance_evaluation_agent,
            'agent_improvement': builder_gpt.agent_improvement_agent,
            'testing': builder_gpt.testing_agent,
            'deployment': builder_gpt.deployment_agent,
            'strategy_evaluation': builder_gpt.strategy_evaluation_agent,
        })

    def add_task(self, task_description):
        self.task_queue.append(task_description)

    def run(self):
        while True:
            if self.task_queue:
                task_description = self.task_queue.pop(0)
                print(f"Processing task: {task_description}")
                result = self.builder_gpt.execute(task_description)
                self.completed_tasks.append((task_description, result))
                print(f"Completed task: {task_description}")
            else:
                print("No tasks in queue. Waiting for new tasks...")
                time.sleep(5)

            # Self-improvement loop
            self.optimize_agents()
            self.evaluate_system_performance()

    def optimize_agents(self):
        print("Optimizing agents...")
        agent_list = [agent for agent in self.builder_gpt.task_manager_agent.agents.values()]
        optimized_agents = self.builder_gpt.agent_improvement_agent.recursive_agent_optimization(agent_list)
        print("Optimization complete.")

    def evaluate_system_performance(self):
        print("Evaluating system performance...")
        for agent, result in self.completed_tasks:
            performance_score = self.builder_gpt.evaluate_performance(agent, result)
            self.builder_gpt.performance_metrics[agent] = performance_score
            if performance_score < 0.7:
                self.builder_gpt.improve_agent(agent)
        print("System evaluation complete.")

if __name__ == "__main__":
    # Initialize BuilderGPT
    builder_gpt = BuilderGPT(
        name="BuilderGPT",
        prompt="Improve and develop software engineering related agents.",
        directory="agents"
    )

    # Initialize and run the MetaScript
    meta_script = MetaScript(builder_gpt)
    meta_script.add_task("Develop and optimize a complex neural network model using PyTorch.")
    meta_script.add_task("Refactor and improve existing codebase.")
    meta_script.add_task("Automate software testing for a new project.")
    meta_script.run()