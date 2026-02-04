from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken
from logs.logging_setup import log_action


class ReporterAgent:
    def __init__(self, model_client):
        self.agent = AssistantAgent(
            name="reporter",
            system_message=
                ( """You are the Reporter agent.
                    Your role is to consolidate and present the final output in a clear, concise, and well-organized format.
                    You focus on summarizing results, conclusions, and key reasoning produced by other agents.
                    You do not introduce new ideas or assumptions.
                    You tailor the level of detail and tone based on the target audience to ensure clarity and readability."""
            ),
            model_client=model_client
        )

    async def run(self, content):
        cancellation = CancellationToken()
        response = await self.agent.on_messages(
            [TextMessage(content=content,source="agent")],cancellation
        )

        log_action("Reporter", f"Generated report for input: {content[:50]}... | Output: {response.chat_message.content[:200]}...")

        return response.chat_message.content