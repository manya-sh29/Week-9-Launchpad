import json
from autogen_ext.models.llama_cpp import LlamaCppChatCompletionClient
from autogen_agentchat.agents import AssistantAgent


async def codeExec():
   
    llm_client = LlamaCppChatCompletionClient(
        model_path="src/models/qwen2-7b-instruct-q4_k_m.gguf",
        temperature=0.5,
        n_ctx=32768,
        max_tokens=512,
        verbose=False,
    )

    planner_agent = AssistantAgent(
        name="PlannerAgent",
        system_message="""
You are a Planner (Orchestrator) Agent.

Your responsibility:
- Take the user query
- Break it into smaller, independent subtasks
- Organize the subtasks as a DAG (Directed Acyclic Graph)

Rules:
- You must NOT answer the user query directly
- You must NOT execute tasks
- You must ONLY plan tasks

DAG Requirements:
- Each task must have:
  - task_id
  - description
  - depends_on (list of task_ids)
- Tasks with no dependencies can run in parallel
- No cycles are allowed

Output format (STRICT JSON):
{
  "query": "<original user query>",
  "nodes": [
    {
      "task_id": "T1",
      "description": "<task description>",
      "depends_on": []
    }
  ]
}
""",
        model_client=llm_client,
    )


    result = await planner_agent.run(task="I want to start a cloud kitchen")

    dag = json.loads(result.messages[-1].content)

    return dag

