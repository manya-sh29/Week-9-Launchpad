import asyncio
from agents.research_agent import research_agent
from agents.summarizer_agent import summarizer_agent
from agents.answer_agent import answer_agent

async def main():
    # Step 1: Research Agent
    research_output = await research_agent.run(task="how are you???")  
    print("\n===== RESEARCH OUTPUT =====\n")
    research_text = research_output.messages[-1].content
    print(research_text)

    # Step 2: Summarizer Agent
    summary_output = await summarizer_agent.run(task=research_text)  
    print("\n===== SUMMARY OUTPUT =====\n")
    summarizer_text = summary_output.messages[-1].content
    print(summarizer_text)


    # Step 3: Answer Agent
    final_answer = await answer_agent.run(task=summarizer_text)  
    print("\n===== FINAL ANSWER =====\n")
    answer_text = final_answer.messages[-1].content
    print(answer_text)

if __name__ == "__main__":
    asyncio.run(main())
