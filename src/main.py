#Day3
# from src.tools_orchestrator import run_orchestration,summarize_results
# from src.agents.answer_agent import answer_agent
# import asyncio

# async def main():
#     user_query = "Analyze sales.csv and generate top 5 insights"
#     context = await run_orchestration(user_query)
#     final_summary = summarize_results(context)
#     task = f"You have to reply to user query: {user_query}, based on the context available below: \n{final_summary}"
#     result = await answer_agent.run(task=task)
#     print("=== Final Agent Outputs ===")
#     print(result.messages[-1].content)

# if __name__ == "__main__":
#     asyncio.run(main())





#Day4
import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_core.memory import MemoryContent, MemoryMimeType
from autogen_ext.models.openai import OpenAIChatCompletionClient
from memory.agent_memory import AgentMemorySystem
from memory.Agent import create_fact_agent, extract_and_save_facts
import os
from dotenv import load_dotenv

load_dotenv()

async def main():
    print("AI Memory System!")
    print("=" * 60)

    memory_system = AgentMemorySystem(
        session_max_turns=50,
        vector_k=5,
        vector_threshold=0.3,
        db_path="src/memory/long_term_memory.db",
        vector_persist_path="src/memory/vector_store.faiss"
    )
    
    key = os.getenv("groq")

    model_client = OpenAIChatCompletionClient(
        model="openai/gpt-oss-20b",
        api_key=key,
        base_url="https://api.groq.com/openai/v1",
        model_info={
            "family": "oss",
            "vision": False,
            "function_calling": True,
            "json_output": True,
            "structured_output": True,
            "context_length": 4096,
        }
    )
    
    assistant = AssistantAgent(
        name="assistant",
        model_client=model_client,
        memory=[memory_system]
    )
    
    fact_agent = await create_fact_agent(model_client)
    
    conversation_count = 0
    total_user_facts = 0
    total_context_facts = 0
    
    try:
        while True:
            user_input = input("\nYou: ").strip()
            if user_input.lower() in ['exit', 'quit', 'bye']:
                print("\nGoodbye!")
                break
            
            if not user_input:
                continue
            
            conversation_count += 1
            await memory_system.add(
                MemoryContent(
                    content=user_input,
                    mime_type=MemoryMimeType.TEXT,
                    metadata={"role": "user", "turn": conversation_count}
                ),
                store_long_term=False
            )
            
            print("\nAssistant: ", end="", flush=True)
            
            try:
                result = await assistant.run(task=user_input)
                
                response_text = ""
                if result and hasattr(result, 'messages'):
                    for msg in result.messages:
                        if hasattr(msg, 'content') and isinstance(msg.content, str):
                            if msg.source != 'user':
                                print(msg.content)
                                response_text = msg.content
                                break
                
                if response_text:
                    await memory_system.add(
                        MemoryContent(
                            content=response_text,
                            mime_type=MemoryMimeType.TEXT,
                            metadata={"role": "assistant", "turn": conversation_count}
                        ),
                        store_long_term=False
                    )
                
                if response_text:
                    result = await extract_and_save_facts(
                        fact_agent,
                        user_input,
                        response_text,
                        memory_system
                    )
                    
                    user_facts = result["user_facts"]
                    context_facts = result["conversation_context"]
                    
                    if user_facts == 0 and context_facts == 0:
                        print("No new facts")
                    
                    total_user_facts += user_facts
                    total_context_facts += context_facts
                
            except Exception as e:
                print(f"\nError: {e}")
                continue
    
    except KeyboardInterrupt:
        print("\n\nInterrupted")
    
    finally:
        print("\n" + "=" * 60)
        print("Memory Statistics")
        print("=" * 60)
        
        stats = memory_system.get_memory_stats()
        
        print(f"\nSession:")
        print(f"   - Turns: {conversation_count}")
        
        print(f"\nVector Store (Similarity Search):")
        print(f"   - Total vectors: {stats['vector']['size']}")
        
        print(f"\nLong-term Memory:")
        print(f"   - Total: {stats['long_term']['total_memories']}")
        print(f"   - Semantic (user facts): {stats['long_term']['semantic']}")
        print(f"   - Episodic (conversation): {stats['long_term']['episodic']}")
        
        print(f"\nThis Session:")
        print(f"   - User facts saved: {total_user_facts}")
        print(f"   - Context saved: {total_context_facts}")
        
        await model_client.close()
        await memory_system.close()

asyncio.run(main())