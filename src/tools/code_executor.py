import os
import asyncio
from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import ToolCallSummaryMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.tools.code_execution import PythonCodeExecutionTool
from autogen_ext.code_executors.local import LocalCommandLineCodeExecutor

load_dotenv()

api_key = os.getenv("groq")

model_client = OpenAIChatCompletionClient(
    model="openai/gpt-oss-20b",
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1",
    model_info={
        "family": "oss",
        "vision": False,
        "function_calling": True,
        "json_output": True,
        "structured_output": True,
        "context_length": 4096,
    },
)

async def code_executor(task_description: str, work_dir: str = "./code_output", timeout: int = 600):
    """
    Executes Python code based on a natural-language task description.
    Generates a script, runs it, and returns the printed output.
    """

    os.makedirs(work_dir, exist_ok=True)

    executor = LocalCommandLineCodeExecutor(work_dir=work_dir, timeout=timeout)
    python_tool = PythonCodeExecutionTool(executor)

    agent = AssistantAgent(
        name="PythonCodeExecutorAgent",
        tools=[python_tool],
        model_client=model_client,
        system_message=(
            "You are a Python code executor.\n"
            "- Generate valid Python code based on the task description.\n"
            "- Do not hardcode results; calculations must be executed.\n"
            "- Prefer using print() to output results.\n"
            "- Ensure scripts are readable and well-structured."
        )
    )

    result = await agent.run(task=task_description)

    for msg in result.messages:
        if isinstance(msg, ToolCallSummaryMessage):
            return msg.content

    return "No output produced by the Python code execution."
