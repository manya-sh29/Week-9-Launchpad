from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken
from logs.logging_setup import log_action


class CoderAgent:
    def __init__(self, model_client):
        self.agent = AssistantAgent(
            name="coder",
            system_message=(
                """You are a Coder agent.
                Your role is to design, write, and explain code solutions based on given requirements.
                You focus on correctness, readability, and efficiency of the implementation.
                You translate ideas and logic into executable code.
                You may suggest improvements, optimizations, and best practices when relevant.
                Your responses should primarily consist of clear, well-structured code with concise explanations."""
            ),
            model_client=model_client
        )

    async def run(self, content):
        cancellation = CancellationToken()
        response = await self.agent.on_messages(
            [TextMessage(content=content, source="agent")], cancellation
        )
               
        log_action("Coder", f"Ran coding task with input: {content[:50]}... | Output: {response.chat_message.content[:50]}...")

        return response.chat_message.content
