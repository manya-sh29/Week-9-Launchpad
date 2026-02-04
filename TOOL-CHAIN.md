    # DAY 3 — Tool-Calling Agents (Code, Files, Database, Search)


    ### Objective
    Create **three independent tool-using agents** and an **orchestrator** that coordinates them to solve user queries.

    ---

    ### Agents to Build

    | Agent Name | Tool Used | Description |
    |-----------|----------|-------------|
    | Code Agent | Python Execution | Runs Python code for analysis and computation |
    | DB Agent | SQLite + SQL | Queries structured data from a database |
    | File Agent | File I/O | Reads and writes `.txt` and `.csv` files |

    ---



    ## Agents and Their Responsibilities

    ### File Agent
    **Purpose:**
    Handles all file-related operations.

    **Responsibilities:**
    - Locate files in the local directory structure
    - Detect file types based on extensions
    - Read data from `.csv` and `.txt` files
    - Write processed output to files when required

    **Supported File Types:**
    - `.csv` — structured tabular data
    - `.txt` — unstructured text data

    ---

    ### Code Agent
    **Purpose:**
    Executes Python code for data processing and analysis.

    **Responsibilities:**
    - Perform calculations and transformations
    - Analyze data received from the File Agent
    - Generate insights, summaries, or metrics
    - Return processed results to the orchestrator

    ---

    ### DB Agent
    **Purpose:**
    Interacts with structured databases.

    **Responsibilities:**
    - Connect to SQLite databases
    - Execute SQL queries
    - Fetch and filter data based on query logic
    - Return query results for further analysis

    ---

    ### Example Workflow

    **User Input:**
    Analyze sales.csv and generate top 5 insights


    **Agent Execution Flow:**
    1. Orchestrator assigns **File Agent** to read `sales.csv`
    2. **Code Agent** processes and analyzes the data
    3. **DB Agent** (if needed) queries structured records
    4. Orchestrator combines all results
    5. Final response is returned to the user

