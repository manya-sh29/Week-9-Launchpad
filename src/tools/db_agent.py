import sqlite3
from pathlib import Path
from typing import Any, Dict
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv
import os

load_dotenv()

key = os.getenv("groq")

model_info = {
    "family": "oss",
    "vision": False,
    "function_calling": True,
    "json_output": True,
    "structured_output": True,
    "context_length": 4096,
}

model_client = OpenAIChatCompletionClient(
    model="openai/gpt-oss-20b",
    api_key=key,
    base_url="https://api.groq.com/openai/v1",
    model_info=model_info,
    parallel_tool_calls=False,
)

BLOCKED_SQL = ["UPDATE", "DELETE", "DROP", "ALTER", "TRUNCATE", "ATTACH", "DETACH", "PRAGMA"]
DB_PATH = Path("./src/sales.db")


def _check_sql_safety(sql: str, allow_write: bool = False) -> str:
    sql_upper = sql.upper()
    for word in BLOCKED_SQL:
        if word in sql_upper:
            return f"Forbidden SQL detected: {word}"
    if sql_upper.startswith("INSERT") and not allow_write:
        return "INSERT blocked: write permission not granted"
    if not (sql_upper.startswith("SELECT") or sql_upper.startswith("INSERT")):
        return "Only SELECT and INSERT queries allowed"
    if sql_upper.startswith("SELECT") and "LIMIT" not in sql_upper:
        return "SELECT queries must include LIMIT"
    return ""


async def db_agent(input: str, allow_write: bool = False) -> Dict[str, Any]:
  

    agent = AssistantAgent(
        name="DB_Agent",
        model_client=model_client,
        system_message=(
            "You are a Safe SQLite DB agent.\n"
            "Rules:\n"
            "- Generate ONLY valid SQL\n"
            "- Only SELECT or INSERT queries allowed\n"
            "- SELECT must include LIMIT\n"
            "- No UPDATE, DELETE, DROP, ALTER, etc.\n"
            "- Output ONLY the SQL query"
        ),
    )

    response = await agent.run(task=input)
    sql_text = response.messages[-1].content.strip()

    safety_msg = _check_sql_safety(sql_text, allow_write)
    if safety_msg:
        return {"user_input": input, "sql": sql_text, "error": safety_msg}

    conn = sqlite3.connect(DB_PATH)
    try:
        cursor = conn.execute(sql_text)
        if cursor.description:  
            columns = [d[0] for d in cursor.description]
            rows = cursor.fetchall()
            result = {"rows": [dict(zip(columns, r)) for r in rows], "row_count": len(rows)}
        else: 
            conn.commit()
            result = {"rows_affected": cursor.rowcount}
    except Exception as e:
        result = {"execution_error": str(e)}
    finally:
        conn.close()

    return {"user_input": input, "sql": sql_text, "result": result}
