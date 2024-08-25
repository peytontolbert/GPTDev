# agents/deployment_agent.py

from agents.base_agent import Agent
import docker
import git

class DeploymentAgent(Agent):
    def __init__(self, name, directory):
        super().__init__(name)
        self.directory = directory
        self.docker_client = docker.from_env()
        self.git_repo = git.Repo(self.directory)

    def execute(self, agent_name):
        dockerfile_content = self.generate_dockerfile(agent_name)
        self.save_to_file(f"{self.directory}/Dockerfile", dockerfile_content)
        self.docker_client.images.build(path=self.directory, tag=f"{agent_name}:latest")
        self.push_to_repository(agent_name)

    def generate_dockerfile(self, agent_name):
        dockerfile_prompt = f"Generate a Dockerfile for the following Python agent:\n{agent_name}"
        return self.gpt.chat_with_ollama(dockerfile_prompt, self.prompt)

    def push_to_repository(self, agent_name):
        self.git_repo.git.add(A=True)
        self.git_repo.index.commit(f"Deploy agent: {agent_name}")
        origin = self.git_repo.remote(name='origin')
        origin.push()
