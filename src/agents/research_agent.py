from autogen_ext.models.llama_cpp import LlamaCppChatCompletionClient
from autogen_agentchat.agents import AssistantAgent

# LLM Client
llm_client = LlamaCppChatCompletionClient(
    model_path="src/models/qwen2-7b-instruct-q4_k_m.gguf",
    temperature=0.5,
    n_ctx=32768,
    max_tokens=512,
    verbose=False
)

# Research Agent
research_agent = AssistantAgent(
    name="ResearchAgent",
    system_message="""
You are a Research Agent.
Your job is to collect factual, detailed information.
Do NOT summarize or answer the user.
Output only raw research.

User asked: What is KV caching?
"""
    ,
    model_client=llm_client,
)
