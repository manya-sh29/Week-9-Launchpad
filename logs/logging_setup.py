import logging
import os

os.makedirs("logs", exist_ok=True)

logger = logging.getLogger("nexus_ai")
logger.setLevel(logging.INFO)

if not logger.handlers:
    file_handler = logging.FileHandler("logs/nexus_ai.log")
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(agent)s | %(message)s")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

def log_action(agent_name: str, action_desc: str):
    logger.info(action_desc, extra={"agent": agent_name})
