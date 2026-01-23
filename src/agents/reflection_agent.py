from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.llama_cpp import LlamaCppChatCompletionClient


class ReflectionAgent:
   
    def __init__(self):
        self.llm_client = LlamaCppChatCompletionClient(
            model_path="src/models/qwen2-7b-instruct-q4_k_m.gguf",
            temperature=0.3,
            n_ctx=32768,
            max_tokens=512,
            verbose=False,
        )

        self.reflector_agent = AssistantAgent(
            name="ReflectionInternalAgent",
            system_message="""
You are a Reflection Agent.

Your responsibility:
- Review the worker's output
- Improve clarity, structure, and correctness
- Fix mistakes if any
- DO NOT introduce new information
- DO NOT validate formally
- DO NOT plan or execute tasks

Output ONLY the improved response.
""",
            model_client=self.llm_client,
        )

    async def reflect(self, worker_output: dict) -> dict:
        """
        worker_output format:
        {
            "task_id": "T1",
            "result": "<worker generated text>"
        }

        Returns:
        {
            "task_id": "T1",
            "reflected_result": "<improved text>"
        }
        """

        prompt = f"""
Worker Output:
{worker_output['result']}

Reflect and improve the above output.
"""

        reflection_result = await self.reflector_agent.run(task=prompt)

        reflected_text = reflection_result.messages[-1].content

        print(f"Reflection Output for {worker_output['task_id']}:\n{reflected_text}\n")

        return {
            "task_id": worker_output["task_id"],
            "reflected_result": reflected_text
        }
