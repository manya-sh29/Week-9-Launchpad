from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken
from logs.logging_setup import log_action


class OptimizerAgent:
    def __init__(self, model_client):
        self.agent = AssistantAgent(
            name="optimizer",
            system_message=
                ("""You are the Optimizer agent.
                    Your role is to improve existing solutions by optimizing performance, cost, scalability, memory usage, or simplicity.
                    You do not alter core requirements or functionality.
                    You clearly explain the trade-offs of any optimization you propose.
                    You prioritize measurable improvements while maintaining clarity and maintainability."""
            ),
            model_client=model_client
        )

    async def run(self, content):
        cancellation = CancellationToken()
        response = await self.agent.on_messages(
            [TextMessage(content=content,source="agent")],cancellation
        )

        log_action("Optimizer", f"Optimized content: {content[:50]}... | Output: {response.chat_message.content[:50]}...")

        return response.chat_message.content