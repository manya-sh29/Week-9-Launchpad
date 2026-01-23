import asyncio

from src.orchestrator.planner import codeExec
from src.agents.worker_agent import WorkerAgent
from src.agents.reflection_agent import ReflectionAgent
from src.agents.validator_agent import ValidatorAgent


async def execute_dag_workers_only(dag):
    worker_agent = WorkerAgent()
    results = {}  
    for node in dag["nodes"]:
        task_id = node["task_id"]
        description = node["description"]
        depends_on = node.get("depends_on", [])

        dependency_outputs = {
            dep_id: results[dep_id]
            for dep_id in depends_on
        }

        worker_output = await worker_agent.execute_task({
            "task_id": task_id,
            "description": description,
            "dependency_outputs": dependency_outputs
        })

        results[task_id] = worker_output

    return results


async def main():
    dag = await codeExec()
    print("\nDAG FROM PLANNER:\n", dag)

    worker_results = await execute_dag_workers_only(dag)

    reflection_agent = ReflectionAgent()
    reflected_output = await reflection_agent.reflect(worker_results)

    validator_agent = ValidatorAgent()
    final_output = await validator_agent.validate(reflected_output)

    print("\nFINAL OUTPUT:\n", final_output)


if __name__ == "__main__":
    asyncio.run(main())
