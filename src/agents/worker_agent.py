from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.llama_cpp import LlamaCppChatCompletionClient
from src.agents.reflection_agent import ReflectionAgent


class WorkerAgent:

    def __init__(self):
        self.llm_client = LlamaCppChatCompletionClient(
            model_path="src/models/qwen2-7b-instruct-q4_k_m.gguf",
            temperature=0.4,
            n_ctx=32768,
            max_tokens=512,
            verbose=False,
        )

        self.worker_llm_agent = AssistantAgent(
            name="WorkerInternalAgent",
            system_message="""
You are a Worker Agent.

Rules:
- Execute ONLY the given subtask
- Do NOT plan
- Do NOT validate
- Do NOT send to any other agent
- Produce a clear and direct answer
""",
            model_client=self.llm_client,
        )

    async def execute_task(self, task: dict) -> dict:

        worker_result = await self.worker_llm_agent.run(task=task["description"])

        completed_output = worker_result.messages[-1].content

        print(f"Worker Output for {task['task_id']}:\n{completed_output}\n")

        return {
            "task_id": task["task_id"],
            "result": completed_output
        }
    


