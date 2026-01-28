from src.tools_orchestrator import run_orchestration,summarize_results
from src.agents.answer_agent import answer_agent
import asyncio

async def main():
    user_query = "Analyze sales.csv and generate top 5 insights"
    context = await run_orchestration(user_query)
    final_summary = summarize_results(context)
    task = f"You have to reply to user query: {user_query}, based on the context available below: \n{final_summary}"
    result = await answer_agent.run(task=task)
    print("=== Final Agent Outputs ===")
    print(result.messages[-1].content)

if __name__ == "__main__":
    asyncio.run(main())