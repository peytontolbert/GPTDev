from agents.analysis.knowledge_retrieval_agent import KnowledgeRetrievalAgent
from agents.analysis.code_review_agent import CodeReviewAgent
from agents.analysis.meta_learning_agent import MetaLearningAgent
from agents.analysis.exploration_strategy_agent import ExplorationStrategyAgent
from agents.analysis.strategy_evaluation_agent import StrategyEvaluationAgent
from agents.communication.inter_agent_communication_agent import InterAgentCommunicationAgent
from agents.deployment.deployment_agent import DeploymentAgent
from agents.improvement.agent_improvement_agent import AgentImprovementAgent
from agents.integration.dependency_management_agent import DependencyManagementAgent
from agents.management.agent_update_manager_agent import AgentUpdateManager
from agents.management.task_manager_agent import TaskManagerAgent
from agents.performance.performance_evaluation_agent import PerformanceEvaluationAgent
from agents.planning.task_decomposition_agent import TaskDecompositionAgent
from agents.testing.testing_agent import TestingAgent
from agents.management.orchestration_agent import OrchestrationAgent

class AgentInitialization:
    def __init__(self, name, prompt, directory, version_control, knowledge_retrieval_agent):
        self.task_decomposition_agent = TaskDecompositionAgent(name="TaskDecompositionAgent")
        self.knowledge_retrieval_agent = KnowledgeRetrievalAgent(name="KnowledgeRetrievalAgent")
        self.inter_agent_communication_agent = InterAgentCommunicationAgent(name="InterAgentCommunicationAgent")
        self.code_review_agent = CodeReviewAgent(name="CodeReviewAgent")
        self.meta_learning_agent = MetaLearningAgent(name="MetaLearningAgent")
        self.exploration_strategy_agent = ExplorationStrategyAgent(name="ExplorationStrategyAgent")
        self.performance_evaluation_agent = PerformanceEvaluationAgent(name="PerformanceEvaluationAgent", prompt=prompt)
        self.orchestration_agent = OrchestrationAgent(name="OrchestrationAgent")
        self.testing_agent = TestingAgent(name="TestingAgent")
        self.deployment_agent = DeploymentAgent(name="DeploymentAgent", directory=directory)
        self.strategy_evaluation_agent = StrategyEvaluationAgent(name="StrategyEvaluationAgent")
        self.agent_update_manager = AgentUpdateManager(name="AgentUpdateManager", directory=directory, version_control=version_control)
        self.dependency_manager_agent = DependencyManagementAgent(name="DependencyManagerAgent")
        self.agent_improvement_agent = AgentImprovementAgent(name="AgentImprovementAgent", knowledge_retrieval_agent=knowledge_retrieval_agent)

