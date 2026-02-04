import asyncio
from autogen_ext.models.openai import OpenAIChatCompletionClient
from nexus_ai.agents.researcher import ResearcherAgent
from nexus_ai.agents.analyst import AnalystAgent
from nexus_ai.agents.critic import CriticAgent
from nexus_ai.agents.optimizer import OptimizerAgent
from nexus_ai.agents.validator import ValidatorAgent
from nexus_ai.agents.reporter import ReporterAgent
from nexus_ai.agents.planner import PlannerAgent
from nexus_ai.agents.coder import CoderAgent
from nexus_ai.agents.orchestrator import MemoryEnabledOrchestrator
from nexus_ai.memory.memory_agent import AgentMemorySystem
import os
from dotenv import load_dotenv
load_dotenv()

async def main():
    
    print("Multi-Agent System\n")    
    key = os.getenv("groq")
    model_info = {
        "family": "oss",
        "vision": False,
        "function_calling": True,
        "json_output": True,
        "structured_output": True,
        "context_length": 4096,
    }

    model_client = OpenAIChatCompletionClient(
        model="openai/gpt-oss-20b",
        api_key=key,
        base_url="https://api.groq.com/openai/v1",
        model_info=model_info,
    )
    
    memory_system = AgentMemorySystem(
        session_max_turns=50,
        vector_k=5,
        vector_threshold=0.3,
        db_path="nexus_ai/datastorage/agent_long_term.db",
        vector_persist_path="nexus_ai/datastorage/agent_vectors.faiss"
    )
    
    planner = PlannerAgent(model_client)
    researcher = ResearcherAgent(model_client)
    analyst = AnalystAgent(model_client)
    coder = CoderAgent(model_client)
    critic = CriticAgent(model_client)
    optimizer = OptimizerAgent(model_client)
    validator = ValidatorAgent(model_client)
    reporter = ReporterAgent(model_client)
    
    agents = {
        "Researcher": researcher,
        "Analyst": analyst,
        "Coder": coder,
        "Critic": critic,
        "Optimizer": optimizer,
        "Validator": validator,
        "Reporter": reporter
    }
    
    orchestrator = MemoryEnabledOrchestrator(
        planner_agent=planner,
        agents_dict=agents,
        memory_system=memory_system
    )
    
    tasks = [
        "Plan a startup in AI for healthcare",
    ]
    
    for task in tasks:
        result = await orchestrator.execute(task, use_memory=True)
        
        print("\n" + "="*70)
        print("FINAL OUTPUT")
        print("="*70)
        print(result)
        print("\n" + "="*70)
        
        stats = await orchestrator.get_memory_stats()
        print(f"\nMemory Stats: {stats}\n")
    
    await memory_system.close()


if __name__ == "__main__":
    asyncio.run(main())