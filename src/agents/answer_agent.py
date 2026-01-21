from autogen_ext.models.llama_cpp import LlamaCppChatCompletionClient
from autogen_agentchat.agents import AssistantAgent

llm_client = LlamaCppChatCompletionClient(
    model_path="src/models/qwen2-7b-instruct-q4_k_m.gguf",
    temperature=0.5,
    n_ctx=32768,
    max_tokens=512,
    verbose=False
)

answer_agent = AssistantAgent(
    name="AnswerAgent",
    system_message="""
You are an Answer Agent.

Your responsibility:
- Read the summary provided by the Summarizer Agent.
- Provide a clear, concise, and factual answer to the user.
- Do NOT add new information beyond the summary.
- Format the answer in simple and easy-to-understand language.
"""
    ,
    model_client=llm_client,
)
