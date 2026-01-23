from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.llama_cpp import LlamaCppChatCompletionClient


class ValidatorAgent:
   
    def __init__(self):
        self.llm_client = LlamaCppChatCompletionClient(
            model_path="src/models/qwen2-7b-instruct-q4_k_m.gguf",
            temperature=0.2,
            n_ctx=32768,
            max_tokens=512,
            verbose=False,
        )

        self.validator_agent = AssistantAgent(
            name="ValidatorInternalAgent",
            system_message="""
You are a Validator Agent.

Your responsibility:
- Review the reflected output from the worker
- Check for correctness, clarity, and completeness
- Fix minor errors if needed
- DO NOT plan new tasks
- DO NOT execute tasks
- Return the fully validated text as final output
""",
            model_client=self.llm_client,
        )

    async def validate(self, reflected_output: dict) -> dict:
        """
        reflected_output format:
        {
            "task_id": "T1",
            "reflected_result": "<reflected text>"
        }

        Returns:
        {
            "task_id": "T1",
            "final_output": "<validated, final text>"
        }
        """

        prompt = f"""
Reflected Output:
{reflected_output['reflected_result']}

Check correctness, clarity, completeness and fix any minor errors.
Provide the final validated text.
"""

        validation_result = await self.validator_agent.run(task=prompt)

        final_text = validation_result.messages[-1].content

        print(f"Validator Output for {reflected_output['task_id']}:\n{final_text}\n")

        return {
            "task_id": reflected_output["task_id"],
            "validator_output": final_text
        }
