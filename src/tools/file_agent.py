from autogen_ext.agents.file_surfer import FileSurfer
from autogen_ext.models.ollama import OllamaChatCompletionClient
from autogen_core.tools import FunctionTool
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.agents import AssistantAgent
import os
import asyncio
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.tools import AgentTool
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

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
        model="qwen/qwen3-32b",
        api_key=key,
        base_url="https://api.groq.com/openai/v1",
        model_info=model_info,
        parallel_tool_calls=False
    )

file_surfer = FileSurfer(name="FILE_AGENT",
                          model_client=model_client,
                          base_path="./src/data")

def detect_file_type(file_path: str):
    path = Path(file_path)
    if not path.exists():
        return "File not found"
    return path.suffix.lower() 

file_surfer_tool = AgentTool(agent=file_surfer, return_value_as_last_message=True)

async def file_agent(input: str):
    agent = AssistantAgent(
        name="File_Agent",
        model_client=model_client,
        tools=[file_surfer_tool],
        system_message=(
            "You are a file agent. "
            "You can retrieve the absolute path of files in the directory using file surfer tool. "
            "Process the input query and output the location of the files requested by the user. "
        )
    )
    response = await agent.run(task=input)
    return response.messages[-1].content


