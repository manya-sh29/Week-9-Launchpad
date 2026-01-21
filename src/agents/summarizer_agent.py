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

# Summarizer Agent
summarizer_agent = AssistantAgent(
    name="SummarizerAgent",
    system_message="""
You are a Summarizer Agent.

Your responsibilities:
- Convert research content into a short, structured summary.
- Preserve factual accuracy.
- Remove redundancy and noise.
- Do NOT add new information.
- Do NOT answer the end user.

Output format:
- Bullet points
- Clear headings if needed
- Concise and neutral tone
"""
    ,
    model_client=llm_client,
)
